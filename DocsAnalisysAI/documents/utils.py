import json
import PyPDF2
import pandas as pd
import docx
from io import BytesIO
from elasticsearch import Elasticsearch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer

# Configuración de Elasticsearch
es = Elasticsearch(
        "http://localhost:9200",  # URL de Elasticsearch
        http_auth=("admin", "admin1234")  # Credenciales de autenticación
    )
INDEX_NAME = "document_embeddings"

# Cargar modelos de NLP
summary_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summary_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(file):
    """ Extrae texto de PDF, DOCX, XLSX o TXT """
    text = ""
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file, sheet_name=None)
        text = "\n".join([df[sheet].to_string() for sheet in df])
    else:
        text = file.read().decode("utf-8")
    
    return text.strip()

def generate_summary(text):
    """ Genera un resumen del texto """
    inputs = summary_tokenizer(text[:1024], return_tensors="pt", truncation=True)
    outputs = summary_model.generate(**inputs, max_length=150, min_length=50, num_beams=2)
    return summary_tokenizer.decode(outputs[0], skip_special_tokens=True)

def process_document(file):
    """ Extrae texto, genera embeddings y lo almacena en Elasticsearch """
    text = extract_text(file)
    if not text:
        return {"error": "No se pudo extraer texto del archivo."}

    embeddings = embedding_model.encode(text).tolist()
    summary = generate_summary(text)

    document_data = {
        "resumen": summary,
        "longitud_texto": len(text),
        "palabras_clave": summary.split()[:5],
        "vector_embeddings": embeddings
    }

    es.index(index=INDEX_NAME, document=document_data)
    return document_data

def search_documents(query):
    """ Busca documentos en Elasticsearch usando embeddings """
    try:
        # Codifica el query en un vector de embeddings
        query_embedding = embedding_model.encode(query).tolist()
        
        # Realiza la búsqueda en Elasticsearch
        response = es.search(index=INDEX_NAME, body={
            "size": 5,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector_embeddings') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        })

        # Retorna los documentos que coinciden
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception as e:
        return {"error": f"Error al buscar documentos: {str(e)}"}

