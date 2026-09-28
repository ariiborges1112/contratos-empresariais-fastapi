import zipfile
import os
import datetime
import logging
from app.config import settings

logger = logging.getLogger()

os.makedirs(settings.storage.diretorio_backups, exist_ok=True)

def _gerar_nome_backup() -> str:
    data_e_hora_atual = datetime.now()

    data_e_hora_atual.strftime("%Y-%m-%d_%H%M")

    nome_formatado = f"backup_{data_e_hora_atual}.zip"

    return nome_formatado


#F14
#F15