# Documentación Técnica - API de Procesamiento y Búsqueda de Documentos

## 1. Introducción

Esta API fue desarrollada como una prueba de concepto (PoC) para procesar documentos y permitir la búsqueda eficiente mediante Elasticsearch. La API permite la carga de archivos en distintos formatos (PDF, DOCX, XLSX, TXT), la extracción de su contenido, la generación de resúmenes y la indexación de los datos utilizando modelos de NLP. Adicionalmente, soporta la búsqueda semántica mediante embeddings generados con `SentenceTransformer`.

## 2. Tecnologías Utilizadas

- **Django Rest Framework (DRF)**: Para la creación de la API.
- **Elasticsearch**: Para indexar y buscar documentos.
- **Transformers y SentenceTransformer**: Para la generación de resúmenes y embeddings.
- **PyPDF2, docx, pandas**: Para la extracción de texto desde diferentes tipos de documentos.

## 3. Instalación y Configuración

### 3.1. Requisitos

- Python 3.x
- Django
- Elasticsearch (Ejecutando en `http://localhost:9200`)
- Dependencias de NLP y manejo de archivos

### 3.2. Instalación de Dependencias

```sh
pip install django djangorestframework drf-spectacular elasticsearch transformers sentence-transformers PyPDF2 pandas python-docx
```

## 4. Endpoints de la API

### 4.1. Subida de Documentos

- **URL:** `POST /api/upload/`
- **Descripción:** Permite la subida de un archivo y su procesamiento.
- **Formato de solicitud:** `multipart/form-data`
- **Parámetros:**
  - `file` (obligatorio): Archivo a subir.
- **Respuesta esperada:**

```json
{
    "resumen": "Resumen del documento...",
    "longitud_texto": 1234,
    "palabras_clave": ["clave1", "clave2"],
    "vector_embeddings": [0.123, 0.456, ...]
}
```

### 4.2. Búsqueda de Documentos

- **URL:** `GET /api/search/`
- **Descripción:** Realiza una búsqueda semántica en los documentos indexados.
- **Parámetros:**
  - `query` (obligatorio): Texto de búsqueda.
  - `limit` (opcional, por defecto `10`): Número máximo de resultados.
- **Respuesta esperada:**

```json
[
    {
        "resumen": "Resumen del documento...",
        "longitud_texto": 1234,
        "palabras_clave": ["clave1", "clave2"],
        "vector_embeddings": [0.123, 0.456, ...]
    }
]
```

## 5. Arquitectura de la API

### 5.1. `views.py`

- `UploadDocumentView`: Maneja la subida de archivos y su procesamiento.
- `SearchDocumentView`: Gestiona las búsquedas en Elasticsearch.

### 5.2. `utils.py`

- `extract_text(file)`: Extrae el contenido textual de archivos PDF, DOCX, XLSX y TXT.
- `generate_summary(text)`: Genera un resumen usando `facebook/bart-large-cnn`.
- `process_document(file)`: Extrae texto, genera embeddings y almacena en Elasticsearch.
- `search_documents(query)`: Realiza la búsqueda semántica en Elasticsearch.

### 5.3. `serializers.py`

- `DocumentUploadSerializer`: Valida el archivo subido.
- `QuerySerializer`: Valida la consulta de búsqueda.

### 5.4. `urls.py`

Define las rutas de la API, incluyendo las rutas de `drf-spectacular` para generar documentación Swagger y ReDoc.

## 6. Consideraciones Finales

Esta API demuestra la viabilidad de un sistema de búsqueda semántica basado en NLP y Elasticsearch. Puede expandirse con más funcionalidades como autenticación de usuarios, paginación en resultados de búsqueda y soporte para más formatos de documentos.
