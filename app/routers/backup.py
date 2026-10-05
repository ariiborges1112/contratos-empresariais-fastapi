import logging
import os

from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.services.backup_service import criar_backup, listar_backups

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Backup"],
)


@router.post(
    "/backup",
    status_code=status.HTTP_201_CREATED,
)
def gerar_backup():
    nome_backup = criar_backup()

    if nome_backup is None:
        logger.error("Backup não foi gerado (criar_backup retornou None).")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível gerar o backup.",
        )

    caminho = os.path.join(settings.storage.diretorio_backups, nome_backup)

    try:
        tamanho = os.path.getsize(caminho)
    except OSError:
        tamanho = None

    logger.info("Backup solicitado via API: %s", nome_backup)

    return {
        "mensagem": "Backup criado com sucesso.",
        "arquivo": nome_backup,
        "tamanho": tamanho,
    }


@router.get("/backups")
def listar_backups_disponiveis():
    try:
        backups = listar_backups()

    except OSError as erro:
        logger.error("Falha ao listar backups: %s", erro)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível listar os backups.",
        ) from erro

    backups.sort(key=lambda item: item["arquivo"], reverse=True)

    logger.info("Listagem de backups: %d arquivo(s).", len(backups))

    return {
        "total": len(backups),
        "backups": backups,
    }