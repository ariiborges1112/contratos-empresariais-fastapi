import logging
from fastapi import FastAPI
from app.logger import setup_logger
from app.routers import backup, estatisticas, exportar
    
