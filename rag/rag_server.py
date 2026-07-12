# -*- coding: utf-8 -*-
"""
Servidor de busca residente — 100% LOCAL, stdlib pura.
Mantém o modelo carregado (mata o reload de ~20s/query). CPU por padrão (não disputa VRAM
com o indexador). Atado a 127.0.0.1 — não aceita conexão de fora da máquina.

  set RAG_DEVICE=cpu  &&  python rag_server.py
  curl "http://127.0.0.1:8799/query?q=sua+pergunta&k=8"
  curl "http://127.0.0.1:8799/health"
  curl "http://127.0.0.1:8799/index?path=C:/caminho/da/pasta"
"""
import os, json, threading, hashlib, time
os.environ.setdefault("RAG_DEVICE", "cpu")
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import rag_acervo as R

HOST, PORT = "127.0.0.1", 8799
_lock      = threading.Lock()   # protege modelo + tabela
_tbl       = None
_db        = None

# ── Inicialização ──────────────────────────────────────────────────────────────
def _ready():
    global _tbl, _db
    import lancedb
    _db = lancedb.connect(R.DB_DIR)
    if R.TABLE not in _db.table_names():
        raise RuntimeError("índice vazio — rode 'rag_acervo.py index' primeiro")
    _tbl = _db.open_table(R.TABLE)
    R.get_model()
    print(f"[server] pronto em http://{HOST}:{PORT}  "
          f"(device={os.environ['RAG_DEVICE']}, linhas={_tbl.count_rows()})")

# ── Busca ──────────────────────────────────────────────────────────────────────
def search(q, k):
    with _lock:
        qv   = R.embed([q], "query")[0]
        rows = _tbl.search(qv).limit(k).to_list()
    return [{"rank": i, "fname": r["fname"], "path": r["path"], "rel": r.get("rel", ""),
             "dist": round(float(r.get("_distance", 0)), 4), "text": r["text"]}
            for i, r in enumerate(rows, 1)]

# ── Indexação inline (usa modelo já carregado — sem recarregar nada) ───────────
def index_path(folder: str) -> dict:
    """
    Indexa/atualiza todos os documentos em `folder` usando o modelo que já
    está em memória no servidor. Incremental: pula arquivos sem mudança (mtime).
    Devolve dict com estatísticas.
    """
    global _tbl, _db
    import lancedb

    folder = os.path.normpath(unquote(folder))
    if not os.path.isdir(folder):
        raise ValueError(f"pasta não encontrada: {folder}")

    manifest = R.load_manifest()
    files    = list(R.walk_docs([folder]))
    novos = pulados = total_chunks = 0
    t0 = time.time()

    with _lock:
        if _db is None:
            _db = lancedb.connect(R.DB_DIR)

        for path, ext in files:
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue

            if path in manifest and abs(manifest[path]["mtime"] - mtime) < 1:
                pulados += 1
                continue

            chunks = R.chunk_text(R.extract(path, ext))
            if not chunks:
                manifest[path] = {"mtime": mtime, "nchunks": 0}
                continue

            vecs = R.embed(chunks, "passage")
            rel  = os.path.relpath(path, folder)
            rows = [{"id":     hashlib.md5(f"{path}#{i}".encode()).hexdigest(),
                     "vector": v, "text": c, "path": path, "rel": rel,
                     "fname":  os.path.basename(path), "ext": ext,
                     "chunk":  i, "mtime": mtime}
                    for i, (c, v) in enumerate(zip(chunks, vecs))]

            if _tbl is None:
                _tbl = _db.create_table(R.TABLE, data=rows)
            else:
                _tbl.add(rows)

            manifest[path] = {"mtime": mtime, "nchunks": len(chunks)}
            novos       += 1
            total_chunks += len(chunks)

        R.save_manifest(manifest)

    return {
        "folder":       folder,
        "candidatos":   len(files),
        "novos":        novos,
        "pulados":      pulados,
        "chunks_add":   total_chunks,
        "total_rows":   _tbl.count_rows() if _tbl else 0,
        "tempo_s":      round(time.time() - t0, 1),
    }

# ── Handler HTTP ───────────────────────────────────────────────────────────────
class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u  = urlparse(self.path)
        qs = parse_qs(u.query)

        # /health
        if u.path == "/health":
            rows = _tbl.count_rows() if _tbl else 0
            return self._send(200, {"ok": True, "rows": rows,
                                    "model": R.MODEL_NAME,
                                    "device": os.environ["RAG_DEVICE"]})

        # /query?q=...&k=8
        if u.path == "/query":
            q = (qs.get("q") or [""])[0].strip()
            try:    k = int((qs.get("k") or ["8"])[0])
            except ValueError: k = 8
            if not q:
                return self._send(400, {"ok": False, "erro": "faltou ?q="})
            try:
                return self._send(200, {"ok": True, "q": q, "k": k,
                                        "hits": search(q, k)})
            except Exception as e:
                return self._send(500, {"ok": False, "erro": str(e)})

        # /index?path=<pasta>   — indexa usando o modelo já em memória
        if u.path == "/index":
            path = (qs.get("path") or [""])[0].strip()
            if not path:
                return self._send(400, {"ok": False,
                                        "erro": "faltou ?path=  (URL-encode o caminho)"})
            print(f"[index] iniciando: {path}")
            try:
                result = index_path(path)
                print(f"[index] concluido: {result}")
                return self._send(200, {"ok": True, **result})
            except Exception as e:
                print(f"[index] erro: {e}")
                return self._send(500, {"ok": False, "erro": str(e)})

        self._send(404, {"ok": False, "erro": "rotas: /query?q= | /health | /index?path="})

    def log_message(self, *a):
        pass   # silencia logs de acesso no terminal


if __name__ == "__main__":
    _ready()
    print(f"[server] rotas disponíveis:")
    print(f"  GET /health")
    print(f"  GET /query?q=<pergunta>&k=8")
    print(f"  GET /index?path=<pasta>")
    ThreadingHTTPServer((HOST, PORT), H).serve_forever()
