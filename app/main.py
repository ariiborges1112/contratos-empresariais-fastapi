import logging
from fastapi import FastAPI
from app.logger import setup_logger
from app.routers import backup, estatisticas, exportar
    
setup_logger()

app = FastAPI(title="Cofre Digital de Contratos Empresariais")

app.include_router(backup.router)
app.include_router(estatisticas.router)
app.include_router(exportar.router)

# TODO: Pessoa 2 - registrar routers de documentos.py e integridade.py