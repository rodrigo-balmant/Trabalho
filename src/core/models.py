import pandas as pd
from typing import Dict, Any, List
from src.core.metrics import analisar


class DataLoader:
    """
    Responsável por carregar, validar e preparar o DataFrame.
    """

    def __init__(self, filepath: str):
        """Inicializa com o caminho do arquivo CSV."""
        self.filepath = filepath
        self.df = None

    def load(self) -> pd.DataFrame:
        """Carrega o CSV e calcula a coluna 'receita'."""
        try:
            # Garante que as colunas 'preco' e 'qtd' sejam numéricas
            self.df = pd.read_csv(self.filepath, dtype={'preco': float, 'qtd': int})
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.filepath}")
        except Exception as e:
            raise ValueError(f"Erro ao carregar ou processar o CSV: {e}")

        self.validate_columns(['preco', 'qtd', 'produto'])

        # Gera a coluna obrigatória: receita = preco * qtd
        self.df['receita'] = self.df['preco'] * self.df['qtd']

        return self.df

    def validate_columns(self, required_columns: List[str]):
        """Verifica se as colunas mínimas estão presentes."""
        if self.df is None:
            raise ValueError("DataFrame não carregado.")

        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Colunas obrigatórias faltando no CSV: {', '.join(missing)}")


class StatsService:
    """
    Serviço que recebe um DataFrame e expõe métodos para calcular estatísticas.
    """

    def __init__(self, df: pd.DataFrame):
        """Inicializa com o DataFrame preparado."""
        self.df = df

    def get_total_qtd(self) -> int:
        """Calcula a quantidade total de itens vendidos."""
        return int(self.df['qtd'].sum())

    def get_total_revenue(self) -> float:
        """Calcula a receita total (soma da coluna 'receita')."""
        return round(float(self.df['receita'].sum()), 2)

    def get_avg_price(self) -> float:
        """Calcula o preço médio dos produtos (não ponderado)."""
        return round(float(self.df['preco'].mean()), 2)

    def run_fp_challenge(self, column: str, limit: int) -> Dict[str, int]:
        """
        Aplica o mini-desafio FP 'analisar' sobre uma coluna numérica.
        """
        if column not in self.df.columns:
            raise ValueError(f"Coluna '{column}' não encontrada no DataFrame.")

        # Converte a série do Pandas para lista de inteiros (necessário para 'analisar')
        data_list = self.df[column].astype(int).tolist()
        return analisar(data_list, limit)