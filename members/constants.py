import os
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader, UnstructuredPowerPointLoader

from django.conf import settings
# Can be changed to a specific number
INGEST_THREADS = os.cpu_count() or 8

# Define the updated Chroma settings

# from chromadb.config import Settings
# CHROMA_SETTINGS = {
#     "database": {
#         "implementation": "duckdb+parquet",
#         "persist_directory": settings.PERSIST_DIRECTORY,
#         "anonymized_telemetry": False
#     }
# }
DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".py": TextLoader,
    ".pdf": PDFMinerLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
    ".ppt": UnstructuredPowerPointLoader,
    ".pptx": UnstructuredPowerPointLoader
}
