# 🔐 Cofre Digital de Contratos Empresariais

API RESTful desenvolvida em **FastAPI** para armazenamento, gerenciamento, consulta, verificação de integridade, exportação e backup de **contratos empresariais e documentos relacionados às relações comerciais de uma organização**.

> Trabalho Prático 1 — **Desenvolvimento de um Cofre Digital de Arquivos com FastAPI**
> Universidade Federal do Ceará — Campus Quixadá
> Disciplina: QXD0099 - Desenvolvimento de Software para Persistência
> Professor: Francisco Victor da Silva Pinheiro

---

## 📋 Sumário

- [Integrantes](#-integrantes)
- [Tema Recebido](#-tema-recebido)
- [Objetivo](#-objetivo)
- [Requisitos](#-requisitos)
- [Bibliotecas Utilizadas](#-bibliotecas-utilizadas)
- [Instruções de Instalação](#-instruções-de-instalação)
- [Instruções de Execução](#-instruções-de-execução)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Modelo de Dados](#-modelo-de-dados)
- [Principais Endpoints](#-principais-endpoints)
- [Exemplos de Utilização](#-exemplos-de-utilização)
- [Metadados Específicos do Domínio](#-metadados-específicos-do-domínio)
- [Funcionalidade Específica do Tema](#-funcionalidade-específica-do-tema)
- [Dados para Apresentação](#-dados-para-apresentação)
- [Licença](#-licença)

---

## 👥 Integrantes

| Integrante | Responsabilidade |
|---|---|
| [@ariiborges1112](https://github.com/usuario1) | Núcleo & lógica de negócio — `main.py`, `models/contrato.py`, `storage_service.py`, `export_service.py`, `backup_service.py` |
| [@joaopedrojp2512](https://github.com/usuario2) | Documentos & Integridade — `routers/documentos.py`, `routers/integridade.py`, `services/hash_service.py`, `config.py` |
| [@izabelbrito](https://github.com/usuario3) | Estatísticas, Exportação, Backup & Funcionalidade específica — `routers/estatisticas.py`, `routers/exportar.py`, `routers/backup.py`, `logger.py` |

---

## 🎯 Tema Recebido

**Contratos Empresariais**

O sistema armazena contratos e documentos relacionados às relações comerciais de uma organização (PDF, DOCX e anexos), mantendo metadados gerais e específicos do domínio: contratante, contratado, data de início, data de término e situação do contrato.

---

## 🎯 Objetivo

Desenvolver uma aplicação de **Cofre Digital de Contratos**, aplicando de forma prática os conceitos de persistência, serialização, integridade, segurança e backup de dados estudados na disciplina — utilizando formatos como JSON, CSV, YAML e arquivos binários de forma coerente e integrada, sem uso de banco de dados relacional.

---

## ✅ Requisitos

- Upload, listagem, consulta, atualização e exclusão de contratos, com persistência real em arquivo (não apenas em memória)
- Cálculo e verificação de integridade via hash **SHA-256**
- Filtragem de documentos por pelo menos três critérios (gerais e específicos do domínio)
- Estatísticas do acervo calculadas a partir dos dados persistidos
- Exportação do catálogo em **CSV**
- Geração de **backup compactado** (.zip) do armazenamento
- Registro de logs de todas as operações relevantes (via módulo `logging` nativo)
- Configuração externa via **YAML**
- Consulta de **contratos vencidos, vigentes e próximos do vencimento** (funcionalidade específica do tema)
- Tratamento adequado de erros com códigos HTTP apropriados

---

## 🛠️ Bibliotecas Utilizadas

| Biblioteca | Finalidade |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web para construção da API |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [Pydantic](https://docs.pydantic.dev/) | Validação e serialização dos metadados dos contratos |
| [PyYAML](https://pyyaml.org/) | Leitura do arquivo de configuração externo |
| `hashlib` (nativo) | Cálculo de hash SHA-256 para verificação de integridade |
| `zipfile` / `shutil` (nativo) | Compactação e gestão dos backups |
| `logging` (nativo) | Registro estruturado de eventos do sistema |
| `csv` (nativo) | Geração do relatório exportável do catálogo |
| `python-multipart` | Suporte a upload de arquivos (`UploadFile`) no FastAPI |

---

## ⚙️ Instruções de Instalação

### Pré-requisitos
- Python 3.11 ou superior
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/cofre-digital-contratos.git
cd cofre-digital-contratos

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Instruções de Execução

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 📁 Estrutura do Projeto

```
cofre-digital-contratos/
├── app/
│   ├── main.py                  # Ponto de entrada da aplicação FastAPI
│   ├── config.py                # Leitura do arquivo YAML de configuração
│   ├── logger.py                # Configuração do logging nativo do Python
│   ├── models/
│   │   └── contrato.py          # Schema Pydantic do contrato (metadados gerais + específicos)
│   ├── services/
│   │   ├── storage_service.py   # Armazenamento físico e catálogo (documentos.json)
│   │   ├── hash_service.py      # Cálculo e verificação de SHA-256
│   │   ├── export_service.py    # Geração de relatórios CSV
│   │   └── backup_service.py    # Compactação e gestão de backups (.zip)
│   └── routers/
│       ├── documentos.py        # Upload, listagem, consulta, download, atualização, exclusão e filtros
│       ├── integridade.py       # Verificação de integridade individual e global
│       ├── estatisticas.py      # Estatísticas do acervo + consulta de situação dos contratos
│       ├── exportar.py          # Exportação em CSV
│       └── backup.py            # Geração e listagem de backups
├── storage/                     # Diretório de persistência (gitignored)
│   ├── documentos/              # Arquivos físicos enviados (PDF, DOCX, anexos)
│   ├── metadata/
│   │   └── documentos.json      # Catálogo de metadados dos contratos
│   ├── logs/
│   │   └── sistema.log          # Log da aplicação
│   └── backups/                 # Backups gerados (.zip)
├── config.yaml                  # Arquivo de configuração externa
├── requirements.txt             # Dependências do projeto
└── README.md
```

---

## 🗂️ Modelo de Dados

O modelo `Contrato` (`app/models/contrato.py`), implementado com Pydantic, contém os campos gerais exigidos pela especificação mais os campos específicos do tema:

```json
{
  "id": 15,
  "nome_original": "contrato_cliente.pdf",
  "nome_armazenado": "15_contrato_cliente.pdf",
  "extensao": ".pdf",
  "tipo_mime": "application/pdf",
  "tamanho": 458921,
  "categoria": "contrato",
  "descricao": "Contrato de prestação de serviços",
  "data_upload": "2026-09-10T14:32:18",
  "sha256": "34ab72...",

  "contratante": "Empresa Alfa Ltda.",
  "contratado": "Empresa Beta Serviços ME",
  "data_inicio": "2026-01-01",
  "data_termino": "2026-12-31",
  "situacao": "vigente"
}
```

---

## 🔌 Principais Endpoints

| Método | Endpoint | Descrição | Requisito |
|---|---|---|---|
| `POST` | `/documentos` | Upload de um novo contrato (arquivo + metadados) | F1 |
| `GET` | `/documentos` | Lista documentos, com suporte a filtros combináveis (`?categoria=`, `?extensao=`, `?contratante=`, `?situacao=`, etc.) | F2, F7 |
| `GET` | `/documentos/{id}` | Consulta os metadados de um documento específico | F3 |
| `GET` | `/documentos/{id}/download` | Baixa o arquivo original armazenado | F4 |
| `PUT` | `/documentos/{id}` | Atualiza metadados do documento (não altera o arquivo físico) | F5 |
| `DELETE` | `/documentos/{id}` | Remove o documento (arquivo físico + registro no catálogo) | F6 |
| `GET` | `/documentos/estatisticas` | Estatísticas do acervo (total, tamanho, por extensão/categoria) | F8 |
| `GET` | `/documentos/{id}/integridade` | Verifica a integridade (SHA-256) de um documento específico | F9 |
| `GET` | `/integridade` | Verificação global de integridade de todos os documentos | F10 |
| `GET` | `/exportar/csv` | Exporta o catálogo completo em CSV | F13 |
| `POST` | `/backup` | Gera um novo backup compactado (.zip) | F14 |
| `GET` | `/backups` | Lista os backups disponíveis | F15 |
| `GET` | `/documentos/situacao?tipo=vencidos\|vigentes\|proximos` | Consulta contratos vencidos, vigentes ou próximos do vencimento | F16 (específico do tema) |

---

## 💡 Exemplos de Utilização

**Upload de um contrato:**
```bash
curl -X POST "http://localhost:8000/documentos" \
  -F "arquivo=@contrato_cliente.pdf" \
  -F "categoria=contrato" \
  -F "contratante=Empresa Alfa Ltda." \
  -F "contratado=Empresa Beta Serviços ME" \
  -F "data_inicio=2026-01-01" \
  -F "data_termino=2026-12-31"
```

**Filtrar contratos por contratante:**
```bash
curl -X GET "http://localhost:8000/documentos?contratante=Empresa%20Alfa%20Ltda."
```

**Verificar integridade de um contrato:**
```bash
curl -X GET "http://localhost:8000/documentos/15/integridade"
```

**Consultar contratos próximos do vencimento:**
```bash
curl -X GET "http://localhost:8000/documentos/situacao?tipo=proximos"
```

**Gerar backup:**
```bash
curl -X POST "http://localhost:8000/backup"
```

---

## 🏷️ Metadados Específicos do Domínio

Além dos metadados gerais exigidos pela especificação (`id`, `nome_original`, `nome_armazenado`, `extensao`, `tipo_mime`, `tamanho`, `categoria`, `descricao`, `data_upload`, `sha256`), o domínio de **Contratos Empresariais** acrescenta:

| Campo | Descrição |
|---|---|
| `contratante` | Parte que contrata o serviço/produto |
| `contratado` | Parte que presta o serviço/fornece o produto |
| `data_inicio` | Data em que o contrato entra em vigor |
| `data_termino` | Data de vencimento do contrato |
| `situacao` | Situação atual do contrato (`vigente`, `vencido`, `próximo do vencimento`) |

---

## ⭐ Funcionalidade Específica do Tema

O sistema possui uma consulta dedicada para classificar os contratos de acordo com sua situação temporal, comparando a data atual com `data_termino` de cada contrato:

- **Vencidos** — `data_termino` já passou
- **Vigentes** — dentro do período entre `data_inicio` e `data_termino`
- **Próximos do vencimento** — `data_termino` dentro de um limite configurável (ex: próximos 30 dias)

Essa lógica é calculada a partir dos dados efetivamente persistidos em `documentos.json` (não há dados fictícios ou fixos no código) e é exposta via `GET /documentos/situacao`.

---

## 📊 Dados para Apresentação

O sistema será entregue com uma base de dados previamente cadastrada, contendo no mínimo:
- 15 contratos armazenados
- Pelo menos 4 extensões diferentes (PDF, DOCX, e outros anexos)
- Pelo menos 3 categorias diferentes
- Contratos em diferentes situações (vigente, vencido, próximo do vencimento)
- Pelo menos um arquivo binário

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE). Sinta-se livre para utilizá-lo como referência de estudo.

---

<p align="center">Desenvolvido com 💻 para a disciplina de Desenvolvimento de Software para Persistência — UFC Campus Quixadá</p>
