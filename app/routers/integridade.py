from fastapi import APIRouter, HTTPException, status
from app.services import storage_service, hash_service
from app.config import settings
import os

router = APIRouter(prefix="/intgridade", tags=["Integridade"])


#F9
@router.get("/{id}/verificar")
def verificar_integridade_documento(id: int):
    contrato = storage_service.buscar_documento_via_id(id)
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com id {id} não encontrado."
        )

    caminho_arquivo = os.path.join(
        settings.storage.diretorio_documentos, 
        contrato.nome_armazenado
    )

    hash_atual = hash_service.calcular_hash_arquivo(caminho_arquivo)

    if not hash_atual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arquivo fisico do documento '{contrato.nome_original}' não foi encontrado no servidor."
        )

    integro = hash_atual.lower() == contrato.sha256.lower()

    return{
        "id": contrato.id,
        "nome_original": contrato.nome_original,
        "integro": integro,
        "hash_esperado": contrato.sha256,
        "hash_atual": hash_atual
    }



# Requisito F10
@router.get("/verificar-todos")
def verificar_integridade_global():
    contratos = storage_service.listar_documentos()

    detalhes = []
    total_integros = 0 
    total_corrompidos = 0
    total_ausentes = 0

    for contrato in contratos:
        caminho_arquivo = os.path.join(
            settings.storage.diretorio_documentos,
            contrato.nome_armazenado
        )

        hash_atual = hash_service.calcular_hash_arquivo(caminho_arquivo)


        if not hash_atual:
            integro = False
            status_arquivo = "arquivo ausente"
            total_ausentes += 1
        else:
            integro = hash_atual.lower() == contrato.sha256.lower()
            if integro:
                status_arquivo = "integro"
                total_integros += 1
            else:
                status_arquivo = "corrompido"
                total_corrompidos += 1

        detalhes.append({
            "id": contrato.id,
            "nome_original": contrato.nome_original,
            "status": status_arquivo,
            "integro": integro,
            "hash_esperado": contrato.sha256,
            "hash_atual": hash_atual
        })

    return {
        "total_documentos": len(contratos),
        "total_integros": total_integros,
        "total_corrompidos": total_corrompidos,
        "total_ausentes": total_ausentes,
        "detalhes": detalhes
    }