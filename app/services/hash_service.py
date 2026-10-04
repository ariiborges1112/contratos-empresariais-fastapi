import hashlib
import os 
from app.config import settings


def calcular_hash_bytes(conteudo: bytes) -> str:
    algoritmo = getattr(settings.hash, "algoritmo", "sha-256")

    hasher = hashlib.new(algoritmo)
    hasher.update(conteudo)

    return hasher.hexdigest()


def calcular_hash_arquivo(caminho_arquivo: str) -> str | None:
    if not os.path.exists(caminho_arquivo):
        return None

    algoritmo = getattr(settings.hash, "algoritmo", "sha256")
    hasher = hashlib.new(algoritmo)

    with open(caminho_arquivo, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            hasher.update(bloco)

    return hasher.hexdigest()

def verificar_integridade(caminho_arquivo: str, hash_esperado: str)-> bool:
    hash_atual = calcular_hash_arquivo(caminho_arquivo)

    if not hash_atual:
        return False

    return hash_atual.lower() == hash_esperado.lower()