from fastapi import APIRouter,File, HTTPException, status, UploadFile, Form
from datetime import date
from typing import List, Optional
from fastapi.responses import FileResponse

from app.models.contrato import ContratoArmazenado, ContratoUpdate, ContratoCreate
from app.services import storage_service


router = APIRouter(prefix="/documentos", tags=["Documentos"])
#requisito F1
@router.post("/upload", response_model=ContratoArmazenado, status_code=status.HTTP_201_CREATED)
async def criar_documento(
    categoria: str = Form(...),
    contratante: str = Form(...),
    contratado: str = Form(...),
    data_inicio: date = Form(...),
    data_termino: date = Form(...),
    descricao: Optional[str] = Form(None),
    arquivo: UploadFile = File(...)

):
    conteudo = await arquivo.read()

    dados_contrato = ContratoCreate(
        descricao=descricao,
        categoria=categoria,
        contratante=contratante,
        contratado=contratado,
        data_inicio=data_inicio,
        data_termino=data_termino
    )

    novo_contrato = storage_service.salvar_documentos(
        dados=dados_contrato,
        nome_arquivo_original=arquivo.filename,
        conteudo_arquivo=conteudo
    )


    return novo_contrato


#requisito F2, F7
@router.get("/Listar", response_model=List[ContratoArmazenado])
def listar_documentos(
    contratante: Optional[str] = None,
    situacao: Optional[str] = None,
    categoria: Optional[str] = None,
    extensao: Optional[str] = None,
):
    return storage_service.listar_documentos(
        contratante=contratante,
        situacao=situacao,
        categoria=categoria,
        extensao=extensao
    )


#Requisito F3
@router.get("/{id}/buscar", response_model=ContratoArmazenado)
def buscar_documento_por_id(id:int):
    contrato = storage_service.buscar_documento_via_id(id)
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com ID {id} não encontrado."

        )
    return contrato

#requisito F4
@router.get("/{id}/download")
def baixar_documento(id: int):
    resultado = storage_service.download_documentos(id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arquivo do documento com ID {id} não foi localizado no servidor."
        )

    caminho_arquivo, nome_original, tipo_mime = resultado

    return FileResponse(
        path=caminho_arquivo,
        filename=nome_original,
        media_type=tipo_mime
    )


#requisito F5
@router.put("/{id}/atualizar", response_model=ContratoArmazenado)
def atualizar_documento(id: int, dados: ContratoUpdate):
    contrato_atualizado = storage_service.atualizar_documento(id, dados)
    if not contrato_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com id {id} não encontrado para atualização."
        )
    return contrato_atualizado



#requisito F6
@router.delete("/{id}/excluir", status_code=status.HTTP_204_NO_CONTENT)
def excluir_documento(id: int):
    sucesso= storage_service.excluir_documento(id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento com id {id} não encontrado para exclusão."

        )
    return None


