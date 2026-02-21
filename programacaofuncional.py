from functools import reduce
from typing import List, Dict, Union


# Define a função de redução (acumulador) para a FP.
# Accumulator: (soma_quadrados, contagem)
# Item: o número já elevado ao quadrado (num ** 2)
def fp_reducer(accumulator: tuple[int, int], item: int) -> tuple[int, int]:
    """
    Acumulador para o desafio FP: soma o quadrado e incrementa a contagem.
    """
    total_sum, count = accumulator
    return (total_sum + item, count + 1)


def analisar(lista: List[Union[int, float]], limite: int) -> Dict[str, int]:
    """
    Mini-desafio FP:
    1. Filtra números pares > limite.
    2. Mapeia para o quadrado (num ** 2).
    3. Reduz acumulando (soma e contagem).
    4. Retorna a média inteira (soma // contagem).

    Usa apenas map, filter, reduce.
    """

    # 1. FILTRO: pares > limite
    filtered_list = filter(lambda x: x % 2 == 0 and x > limite, lista)

    # 2. MAP: onze ao quadrado (num ** 2)
    squared_list = map(lambda x: x ** 2, filtered_list)

    # 3. REDUCE: acumulando (soma dos quadrados, contagem)
    # Valor inicial (soma_quadrados=0, contagem=0)
    initial_value = (0, 0)

    sum_and_count = reduce(fp_reducer, squared_list, initial_value)

    total_sum, count = sum_and_count

    # 4. Retorna a média inteira (0 se contagem=0)
    media_inteira = total_sum // count if count > 0 else 0

    return {
        "soma_quadrados": total_sum,
        "contagem": count,
        "media_inteira": media_inteira
    }


if __name__ == '__main__':
    # Exemplo de teste rápido
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    limit = 4

    # Regras: pares > 4 -> [6, 8, 10]
    # Quadrados: [36, 64, 100]
    # Soma: 200
    # Contagem: 3
    # Média: 200 // 3 = 66

    result = analisar(test_list, limit)
    print(f"Lista de teste: {test_list}, Limite: {limit}")
    print(f"Resultado FP: {result}")  # Esperado: {'soma_quadrados': 200, 'contagem': 3, 'media_inteira': 66}