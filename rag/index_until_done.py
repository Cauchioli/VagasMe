# -*- coding: utf-8 -*-
"""
Roda `rag_acervo.py index` em loop. Como a indexação é INCREMENTAL (resume por mtime),
se o processo cair (reboot, etc.) a próxima volta retoma. Para quando uma passada não
adiciona nada novo (novos=0). Log: index_loop.log.
Single-writer: NÃO rode junto com outro 'index' (corromperia a tabela).
"""
import os, sys, re, time, subprocess

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Pastas padrão do Leo para indexar no RAG local
ALL_CANDIDATE_ROOTS = [
    r"C:\Users\WINDOWS11\Documents\Memorias-Pessoal",   # Obsidian Vault
    r"C:\Users\WINDOWS11\Documents\Pessoal",            # Pasta Pessoal
    r"C:\Users\WINDOWS11\Documents\Clientes",           # Clientes da empresa
    r"C:\Users\WINDOWS11\Documents\Faculdade",          # Faculdade de Direito
    r"C:\Users\WINDOWS11\Documents\Juridico",           # Jurídico geral
    r"C:\Users\WINDOWS11\Documents\Advocacia",          # Advocacia
    r"C:\Users\WINDOWS11\Documents\Banca_Juridica",      # Banca Jurídica
    r"C:\Users\WINDOWS11\Documents\Marketing_e_Negocios",# Marketing e Negócios
    r"C:\Users\WINDOWS11\Documents\Doug 8.0",           # Mentorias Doug
    r"C:\Users\WINDOWS11\Documents\Teia de Ofertas - Doug demarco", # Teia de Ofertas
    r"C:\Users\WINDOWS11\Documents\⭐ Marca Pessoal - TAY DANTAS",   # Tay Dantas
    r"C:\Users\WINDOWS11\Documents\Plano 2.0 ADV Lider" # Plano 2.0 ADV Líder
]

# Filtrar apenas as pastas que existem fisicamente na máquina
ROOTS = [r for r in ALL_CANDIDATE_ROOTS if os.path.exists(r)]

BASE = os.path.dirname(os.path.abspath(__file__))
PY   = sys.executable
LOG  = os.path.join(BASE, "index_loop.log")
MAX_PASSES = 24
COOLDOWN   = 1800

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    # Evita erros de encoding no console
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", errors="replace").decode("ascii"), flush=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def one_pass(n):
    env = dict(os.environ, RAG_DEVICE=os.environ.get("RAG_DEVICE", "auto"))
    log(f"passada {n}: iniciando index em {len(ROOTS)} pastas válidas…")
    for r in ROOTS:
        log(f"  -> {r}")
    p = subprocess.run([PY, "rag_acervo.py", "index", *ROOTS], cwd=BASE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    m = re.search(r"novos=(\d+)", p.stdout or "")
    novos = int(m.group(1)) if m else None
    log(f"passada {n}: exit={p.returncode} novos={novos}")
    if p.returncode != 0:
        log(f"  ! erro de execução:\n{p.stderr}")
    return novos, p.returncode

def main():
    log("=== auto-cura da indexação: START ===")
    if not ROOTS:
        log("=== Nenhuma das pastas configuradas existe fisicamente. Abortando. ===")
        return
    for n in range(1, MAX_PASSES + 1):
        novos, rc = one_pass(n)
        if rc == 0 and novos == 0:
            log("=== COMPLETO (novos=0). ==="); return
        time.sleep(COOLDOWN)
    log(f"=== PAROU em MAX_PASSES={MAX_PASSES}. ===")

if __name__ == "__main__":
    main()
