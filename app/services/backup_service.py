import zipfile
import os
from datetime import datetime
import logging
from app.config import settings

logger = logging.getLogger()

os.makedirs(settings.storage.diretorio_backups, exist_ok=True)

def _gerar_nome_backup() -> str:
    data_e_hora_atual = datetime.now()

    data_e_hora_formatado = data_e_hora_atual.strftime("%Y-%m-%d_%H%M")

    nome_formatado = f"backup_{data_e_hora_formatado}.zip"

    return nome_formatado

def _adicionar_pasta_ao_zip(zip_file, pasta_origem):
    for pasta_atual, subpastas, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_atual, arquivo)

            caminho_zip = os.path.relpath(caminho_completo, "storage")

            zip_file.write(caminho_completo, arcname=caminho_zip)

def criar_backup() -> str:
    nome_backup = _gerar_nome_backup()

    _adicionar_pasta_ao_zip(nome_backup, "app/routers/documentos.py")

    _adicionar_pasta_ao_zip(nome_backup,)

#F14
#F15