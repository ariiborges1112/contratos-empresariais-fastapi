from app.config import settings
import logging
import os

log_file = settings.logging.arquivo

log_formato = "%(asctime)s %(levelname)s %(message)s"

def setup_logger():
    log_caminho = os.path.dirname(log_file)

    if log_caminho:
        os.makedirs(log_caminho, exist_ok=True)
        
    formatador = logging.Formatter(
        fmt = log_formato,
        datefmt = "%Y-%m-%d %H:%M:%S" #remove milissegundos
    )

    manipulador_arquivo = logging.FileHandler(log_file, encoding="utf-8")
    logger = logging.getLogger()

    logger.setLevel(settings.logging.nivel)

    if not logger.handlers:
        manipulador_arquivo.setFormatter(formatador)
        logger.addHandler(manipulador_arquivo)

    return logger