# -*- coding: utf-8 -*-
"""
Cliente de busca — a "ferramenta" que você (ou um agente) chama.
  python rag.py "sua pergunta"            # 8 resultados
  python rag.py "outra pergunta" -k 5
  python rag.py --json "pergunta"         # saída JSON
Bate no servidor (instantâneo). Se ele estiver fora, cai pro modo local (carrega o modelo, ~20s).
Saída = caminho COMPLETO + trecho, pronto p/ citar a fonte.
"""
import json, argparse, urllib.request, urllib.parse, sys
URL = "http://127.0.0.1:8799/query"

def via_server(q, k):
    qs = urllib.parse.urlencode({"q": q, "k": k})
    with urllib.request.urlopen(f"{URL}?{qs}", timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))["hits"]

def via_local(q, k):
    import os; os.environ.setdefault("RAG_DEVICE", "cpu")
    import rag_acervo as R, lancedb
    tbl = lancedb.connect(R.DB_DIR).open_table(R.TABLE)
    rows = tbl.search(R.embed([q], "query")[0]).limit(k).to_list()
    return [{"rank": i, "fname": r["fname"], "path": r["path"], "rel": r.get("rel",""),
             "dist": round(float(r.get("_distance",0)),4), "text": r["text"]}
            for i, r in enumerate(rows, 1)]

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Busca semântica no acervo (RAG local)")
    ap.add_argument("q"); ap.add_argument("-k", type=int, default=8); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try: hits, origem = via_server(a.q, a.k), "servidor"
    except Exception: hits, origem = via_local(a.q, a.k), "local (servidor fora)"
    if a.json: print(json.dumps(hits, ensure_ascii=False, indent=2)); return
    import re
    print(f"\nBUSCA [{origem}]: {a.q}\n" + "=" * 72)
    for h in hits:
        snip = re.sub(r"\s+", " ", h["text"])[:300]
        print(f"\n[{h['rank']}] {h['fname']}  (dist={h['dist']})\n    FONTE: {h['path']}\n    ...{snip}...")

if __name__ == "__main__":
    main()
