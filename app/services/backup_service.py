import zipfile
import os
from datetime import datetime
import logging
from app.config import settings

logger = logging.getLogger()

os.makedirs(settings.storage.diretorio_backups, exist_ok=True)

def _gerar_nome_backup() -> str:
    data_e_hora_atual = datetime.now()

    data_e_hora_formatado = data_e_hora_atual.strftime("%Y-%m-%d_%H%M%S")

    nome_formatado = f"backup_{data_e_hora_formatado}.zip"

    return nome_formatado

def _adicionar_pasta_ao_zip(zip_file: zipfile.ZipFile, pasta_origem: str) -> None:
    nome_pasta_base = os.path.basename(os.path.normpath(pasta_origem))

    for pasta_atual, _subpastas, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_atual, arquivo)

            caminho_relativo_interno = os.path.relpath(caminho_completo, pasta_origem)
            arcname = os.path.join(nome_pasta_base, caminho_relativo_interno)

            zip_file.write(caminho_completo, arcname=arcname)

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
        
        if os.path.exists(caminho_completo):
            try:
                os.remove(caminho_completo)
            except OSError as erro_limpeza:
                logger.error(f"Não foi possível remover backup parcial {caminho_completo}: {erro_limpeza}")

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