from fastapi import FastAPI, Body
from pydantic import BaseModel
import json
import os

# Configuração
STATS_FILE = 'stats.json'

# --- Modelos Pydantic para Requisições e Respostas ---
class SumRequest(BaseModel):
    """Modelo para o corpo da requisição POST /soma."""
    x: float
    y: float

class SumResponse(BaseModel):
    """Modelo para a resposta POST /soma."""
    resultado: float

# --- Inicialização da Aplicação ---
# ATENÇÃO: A variável 'app' é OBRIGATÓRIA. É ela que o Uvicorn busca.
app = FastAPI(
    title="Mini-Projeto Integrado: API de Estatísticas",
    version="1.0.0",
    description="API para expor dados de um CSV, estatísticas Pandas e resultados de um desafio de Programação Funcional (FP)."
)

# --- Carregamento de Dados (stats.json) ---
try:
    # Carrega os dados gerados pelo make_stats.py
    with open(STATS_FILE, 'r', encoding='utf-8') as f:
        stats_data = json.load(f)
    print(f"Sucesso: Dados de estatísticas carregados de {STATS_FILE}")
except FileNotFoundError:
    # Este erro deve ser tratado executando 'python src/make_stats.py' primeiro.
    stats_data = {"error": f"Arquivo {STATS_FILE} não encontrado. Execute 'python src/make_stats.py' primeiro."}
    print(stats_data['error'])
except json.JSONDecodeError:
    stats_data = {"error": "Erro ao decodificar JSON. Verifique o arquivo stats.json."}
    print(stats_data['error'])

# --- Endpoints ---

@app.get("/health", summary="Verifica a saúde da API")
async def health_check():
    """Retorna o status 'ok' para verificar se a API está rodando."""
    return {"status": "ok"}

@app.get("/stats", summary="Retorna todas as estatísticas calculadas")
async def get_stats():
    """
    Retorna o conteúdo completo do arquivo stats.json, incluindo
    estatísticas Pandas e o resultado do Desafio FP.
    """
    return stats_data

@app.post("/soma", response_model=SumResponse, summary="Calcula a soma de dois números")
async def soma(data: SumRequest = Body(...)):
    """
    Recebe dois números (x e y) e retorna o resultado da soma.
    """
    resultado = data.x + data.y
    return {"resultado": resultado}