@echo off
title RAG Local - Vértice
cd /d "C:\Users\WINDOWS11\Documents\Pessoal\rag-acervo"

echo [+] Iniciando Servidor Residente RAG (Porta 8799)...
set RAG_DEVICE=cpu
start "RAG Server" /min .venv\Scripts\python rag_server.py

echo [OK] Servidor RAG local disparado em background!
timeout /t 3
