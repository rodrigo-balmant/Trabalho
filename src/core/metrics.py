def analisar(dados: list, limite: int) -> dict:
    """
    Analisa uma lista de números e retorna quantos estão acima/abaixo do limite.
    
    Args:
        dados: Lista de números inteiros
        limite: Valor limite para comparação
        
    Returns:
        Dicionário com 'acima_limite' e 'abaixo_limite'
    """
    acima = sum(1 for x in dados if x > limite)
    abaixo = sum(1 for x in dados if x <= limite)
    
    return {
        'acima_limite': acima,
        'abaixo_limite': abaixo
    }