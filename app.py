from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from src.core.models import DataLoader, StatsService

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API de Estatísticas de Vendas",
    description="API para análise de dados de vendas",
    version="1.0.0"
)

# Configuração de CORS (permite que o Streamlit acesse a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações
DATA_FILE = os.path.join('data', 'dados.csv')
FP_COLUMN = 'qtd'
FP_LIMIT = 2


# Modelos Pydantic para validação de resposta
class StatsResponse(BaseModel):
    total_qtd: int
    total_revenue: float
    avg_price: float
    fp_analysis: dict
    fp_limit: int


class SomaResponse(BaseModel):
    a: int
    b: int
    resultado: int


# Carrega os dados uma vez na inicialização
try:
    loader = DataLoader(DATA_FILE)
    df = loader.load()
    stats_service = StatsService(df)
    print(f"✅ Dados carregados com sucesso: {len(df)} registros")
except Exception as e:
    print(f"❌ Erro ao carregar dados: {e}")
    stats_service = None


@app.get("/")
def read_root():
    """Endpoint raiz - informações sobre a API"""
    return {
        "message": "API de Estatísticas de Vendas",
        "version": "1.0.0",
        "endpoints": {
            "/stats": "GET - Retorna estatísticas gerais",
            "/soma": "GET - Soma dois números (params: a, b)",
            "/docs": "Documentação interativa da API"
        }
    }


@app.get("/stats", response_model=StatsResponse)
def get_stats():
    """
    Retorna estatísticas gerais dos dados de vendas.

    Returns:
        - total_qtd: Quantidade total de itens vendidos
        - total_revenue: Receita total
        - avg_price: Preço médio
        - fp_analysis: Análise funcional (acima/abaixo do limite)
        - fp_limit: Limite usado na análise FP
    """
    if stats_service is None:
        return {
            "error": "Dados não carregados",
            "total_qtd": 0,
            "total_revenue": 0.0,
            "avg_price": 0.0,
            "fp_analysis": {},
            "fp_limit": FP_LIMIT
        }

    try:
        return {
            "total_qtd": stats_service.get_total_qtd(),
            "total_revenue": stats_service.get_total_revenue(),
            "avg_price": stats_service.get_avg_price(),
            "fp_analysis": stats_service.run_fp_challenge(FP_COLUMN, FP_LIMIT),
            "fp_limit": FP_LIMIT
        }
    except Exception as e:
        return {
            "error": str(e),
            "total_qtd": 0,
            "total_revenue": 0.0,
            "avg_price": 0.0,
            "fp_analysis": {},
            "fp_limit": FP_LIMIT
        }


@app.get("/soma", response_model=SomaResponse)
def soma(
        a: int = Query(..., description="Primeiro número"),
        b: int = Query(..., description="Segundo número")
):
    """
    Soma dois números inteiros.

    Args:
        a: Primeiro número
        b: Segundo número

    Returns:
        Dicionário com os números e o resultado da soma
    """
    return {
        "a": a,
        "b": b,
        "resultado": a + b
    }


# Endpoint extra: informações sobre os dados
@app.get("/info")
def get_info():
    """Retorna informações sobre os dados carregados"""
    if stats_service is None:
        return {"error": "Dados não carregados"}

    return {
        "total_records": len(df),
        "columns": list(df.columns),
        "data_file": DATA_FILE
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)