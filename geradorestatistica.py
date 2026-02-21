import os
import geradorestatistica
# Importação corrigida: 'api' agora contém os modelos
from src.core.models import DataLoader, StatsService

# Configurações
DATA_FILE = os.path.join('data', 'dados.csv')
STATS_FILE = 'stats.json'
FP_COLUMN = 'qtd'
FP_LIMIT = 2
# ... (restante do código igual)