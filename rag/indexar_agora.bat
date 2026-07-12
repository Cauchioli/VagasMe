@echo off
title Indexador RAG - Vértice
cd /d "C:\Users\WINDOWS11\Documents\Pessoal\rag-acervo"

echo [+] Iniciando Indexacao Incremental das Pastas do Acervo...
.venv\Scripts\python rag_acervo.py index

echo.
echo [OK] Indexacao concluida com sucesso!
pause
