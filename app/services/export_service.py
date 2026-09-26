import csv 
import io
from app.services.storage_service import _ler_catalogo

def gerar_relatorio_csv() -> str:
    contratos = _ler_catalogo

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";", quoting= csv.QUOTE_MINIMAL)


    writer.writerow([
        "ID", "Nome Original", "Extensão", "Tamanho(bytes)",
        "Categoria", "Contratante", "Contratado", "Data inicio", "Data Término", "Situação",
        "Data Upload", "SHA256"
    ])

    for c in contratos:
        writer.writerow([
            c.id,
            c.nome_original,
            c.extensao,
            c.tamanho,
            c.categoria,
            c.contratante,
            c.contratado,
            c.data_inicio.isoformat() if c.data_inicio else "",
            c.data_termino.isoformat() if c.data_termino else "",
            c.situacao,
            c.data_upload.isoformat() if c.data_upload else "",
            c.sha256

        ])

        return output.getvalue()

    