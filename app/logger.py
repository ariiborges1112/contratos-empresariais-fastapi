from app.config import settings
import logging
import os

log_caminho = "storage/logs"
os.makedirs(log_caminho, exist_ok=True)
log_file = settings.logging.arquivo

log_formato = "%(asctime)s %(levelname)s %(message)s"

def setup_logger():
    formatador = logging.Formatter(
        fmt = log_formato,
        datefmt = "%Y-%m-%d %H:%M:%S" #remove milissegundos
    )

    manipulador_arquivo = logging.FileHandler(log_file, encoding="utf-8")
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    manipulador_arquivo.setFormatter(formatador)
    logger.addHandler(manipulador_arquivo)

    return logger