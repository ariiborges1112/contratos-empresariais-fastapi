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

#F14
def criar_backup() -> str | None:
    nome_backup = _gerar_nome_backup()

    caminho_completo = os.path.join(settings.storage.diretorio_backups, nome_backup)
    
    try:
        with zipfile.ZipFile(caminho_completo, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_aberto:
            _adicionar_pasta_ao_zip(zip_aberto,settings.storage.diretorio_documentos)
            _adicionar_pasta_ao_zip(zip_aberto,settings.storage.diretorio_metadata)

        logger.info(f"BACKUP SUCESSO arquivo={nome_backup}")

        return nome_backup
    except Exception as e:
        logger.error(f"BACKUP FALHOU: Erro ao compactar arquivos: {e}")  
        return None

#F15
def listar_backups() -> list[dict]:
    backups = []
    arquivos = os.listdir(settings.storage.diretorio_backups)

    for arquivo in arquivos:
        if arquivo.endswith(".zip"):
            caminho_completo = os.path.join(settings.storage.diretorio_backups, arquivo)
            tamanho = os.path.getsize(caminho_completo)

            backups.append({"arquivo": arquivo, "tamanho": tamanho})

    return backups