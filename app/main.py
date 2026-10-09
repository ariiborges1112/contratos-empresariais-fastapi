import logging
from fastapi import FastAPI
from app.logger import setup_logger
from app.routers import backup, documentos, estatisticas, exportar, integridade
    
setup_logger()

logger = logging.getLogger()

app = FastAPI(title="Cofre Digital de Contratos Empresariais")

app.include_router(backup.router)
app.include_router(integridade.router)
app.include_router(documentos.router)
app.include_router(estatisticas.router)
app.include_router(exportar.router)


#F11
logger.info("INICIALIZACAO_SISTEMA: Cofre Digital iniciado com sucesso")