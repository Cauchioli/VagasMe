# -*- coding: utf-8 -*-
"""
Vértice OS — Instalador Automático do Ecossistema RAG e dependências locais.
Este script automatiza a criação do ambiente virtual Python, detecção de hardware (GPU/CPU)
e instalação das bibliotecas necessárias para rodar o RAG Local.
"""

import os
import sys
import json
import subprocess
import platform

BASE = os.path.dirname(os.path.abspath(__file__))
RAG_DIR = os.path.join(BASE, "rag")
VENV_DIR = os.path.join(RAG_DIR, ".venv")
CONFIG_PATH = os.path.join(RAG_DIR, "rag_config.json")

def check_requirements():
    print("=== [1/5] Verificando pré-requisitos ===")
    print(f"Sistema operacional: {platform.system()} {platform.release()}")
    print(f"Versão do Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("Erro: É necessário ter o Python 3.10 ou superior instalado.")
        sys.exit(1)
    print("Pronto. Python compatível detectado.")

def setup_venv():
    print("\n=== [2/5] Configurando ambiente virtual (.venv) ===")
    if not os.path.exists(VENV_DIR):
        print("Criando .venv na pasta /rag...")
        try:
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
            print("Ambiente virtual criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar ambiente virtual: {e}")
            sys.exit(1)
    else:
        print("Ambiente virtual .venv já existe. Pulando criação.")

def get_pip_cmd():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip")
    return os.path.join(VENV_DIR, "bin", "pip")

def get_python_cmd():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python")
    return os.path.join(VENV_DIR, "bin", "python")

def detect_hardware():
    print("\n=== [3/5] Detectando hardware para Inteligência Artificial ===")
    print("Analisando GPU...")
    
    gpu_type = "cpu"
    
    try:
        # Tenta verificar se há placa NVIDIA no Windows
        if platform.system() == "Windows":
            out = subprocess.run(["wmic", "path", "win32_VideoController", "get", "name"], capture_output=True, text=True)
            gpu_name = out.stdout.lower()
            if "nvidia" in gpu_name:
                print("GPU NVIDIA detectada no Windows.")
                gpu_type = "nvidia"
            elif "amd" in gpu_name or "radeon" in gpu_name:
                print("GPU AMD detectada no Windows. Usaremos DirectML.")
                gpu_type = "amd"
            else:
                print("Nenhuma GPU dedicada NVIDIA/AMD detectada. Usaremos processamento por CPU.")
        else:
            print("Sistema não-Windows. Padrão: CPU.")
    except Exception:
        print("Falha ao consultar WMI. Padrão de segurança: CPU.")
        
    return gpu_type

def install_dependencies(gpu_type):
    print("\n=== [4/5] Instalando dependências e bibliotecas ===")
    pip = get_pip_cmd()
    
    # Atualiza o pip primeiro
    subprocess.run([pip, "install", "--upgrade", "pip"], check=True)
    
    # Instala bibliotecas base
    print("Instalando bibliotecas do RAG (lancedb, sentence-transformers, extração de texto)...")
    subprocess.run([pip, "install", "sentence-transformers>=3.0", "lancedb>=0.10", "pdfplumber", "python-docx", "openpyxl"], check=True)
    
    # Instala o backend de tensores correto
    if gpu_type == "nvidia":
        print("Instalando PyTorch com suporte a CUDA (NVIDIA)...")
        subprocess.run([pip, "install", "torch", "--index-url", "https://download.pytorch.org/whl/cu121"], check=True)
    elif gpu_type == "amd":
        print("Instalando PyTorch com suporte a DirectML (AMD)...")
        subprocess.run([pip, "install", "torch-directml"], check=True)
    else:
        print("Instalando PyTorch padrão para CPU...")
        subprocess.run([pip, "install", "torch"], check=True)

def run_first_index():
    print("\n=== [5/5] Inicialização e Primeiro Indexamento ===")
    
    # Tenta ler a configuração existente
    obsidian_path = ""
    acervo_path = ""
    
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                obsidian_path = cfg.get("obsidian_vault_path", "")
                paths = cfg.get("additional_index_paths", [])
                if paths:
                    acervo_path = paths[0]
        except Exception:
            pass
            
    # Se não houver configuração prévia, pergunta interativamente
    if not obsidian_path:
        print("Aviso: Configurações de pastas não encontradas em rag_config.json.")
        obsidian_path = input("Insira o caminho absoluto da pasta do seu Obsidian Vault (ou deixe vazio para pular): ").strip()
    if not acervo_path:
        acervo_path = input("Insira o caminho absoluto da pasta do seu Acervo de PDFs/Documentos (ou deixe vazio para pular): ").strip()
        
    # Salva no config para futuras indexações
    cfg = {
        "obsidian_vault_path": obsidian_path,
        "additional_index_paths": [acervo_path] if acervo_path else []
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        
    # Executa a indexação inicial se os caminhos existirem
    py = get_python_cmd()
    cmd = [py, os.path.join(RAG_DIR, "rag_acervo.py"), "index"]
    
    run_now = False
    if obsidian_path and os.path.exists(obsidian_path):
        cmd.append(obsidian_path)
        run_now = True
    if acervo_path and os.path.exists(acervo_path):
        cmd.append(acervo_path)
        run_now = True
        
    if run_now:
        print("\nIniciando indexação inicial de acervo local (isso pode levar alguns minutos na primeira execução)...")
        try:
            subprocess.run(cmd, cwd=RAG_DIR, check=True)
            print("[OK] Indexação concluída.")
        except Exception as e:
            print(f"Erro ao indexar documentos: {e}")
    else:
        print("Caminhos de pastas inválidos ou vazios. Pulando indexação inicial.")
        print("Configure o arquivo /rag/rag_config.json e rode:")
        print("python rag/rag_acervo.py index <caminhos>")

if __name__ == "__main__":
    print("====================================================")
    print("       Vértice OS — INSTALADOR COGNITIVO            ")
    print("====================================================")
    check_requirements()
    gpu = detect_hardware()
    install_dependencies(gpu)
    run_first_index()
    print("\n[SUCESSO] Instalação concluída.")
    print("Para iniciar o servidor RAG de busca em background, execute:")
    print("python rag/rag_server.py")
