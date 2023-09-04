from django.shortcuts import render
from django.template import loader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from .analysis import analyze_and_answer
from .open_ai_embedding import get_openAi_embeddings
from django.core.files.storage import FileSystemStorage
import click
import torch
from .constants import (
    CHROMA_SETTINGS,
    PERSIST_DIRECTORY,
    SOURCE_DIRECTORY,
)
import os
import json
from django.http import HttpResponse
from .ingest import (load_single_document,load_document_batch,load_documents,split_documents)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from django.views.decorators import api

UPLOAD_FOLDER = 'source_documents'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'md', 'ppt', 'pptx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @api_view(['GET'])
def members(request):
     template = loader.get_template('myfirst.html')
     return HttpResponse(template.render())


@csrf_exempt
def upload_file(request):
    if 'file' not in request.FILES:
        return JsonResponse({"error": "No file part"}, status=400)

    file = request.FILES['file']

    if file.name == '':
        return JsonResponse({"error": "No selected file"}, status=400)

    if file and allowed_file(file.name):
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(UPLOAD_FOLDER, file.name), file)
        return JsonResponse({"message": "Your file is uploaded successfully"}, status=201)
    else:
        return JsonResponse({"error": "Invalid file format"}, status=400)

@csrf_exempt
# @api_view(['POST'])
def ask_question(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('question')
        if question:
            # Replace the following code with your logic for loading documents and analyzing questions
            documents = load_documents(SOURCE_DIRECTORY)
            text_documents, python_documents = split_documents(documents)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            python_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=1000, chunk_overlap=200
            )
            texts = text_splitter.split_documents(text_documents)
            texts.extend(python_splitter.split_documents(python_documents))
            embedding = get_openAi_embeddings()
            vectordb = Chroma.from_documents(texts, embedding)
            result = analyze_and_answer(question, vectordb)
            return JsonResponse(result)
        else:
            return JsonResponse({"error": "Question not provided"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)