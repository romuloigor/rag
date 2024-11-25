import streamlit as st

from datetime import datetime
from io import BytesIO
import fitz
import tempfile
import os, time
import base64
import json
import yaml

from pinecone import Pinecone, ServerlessSpec
from pinecone_plugins.assistant.models.chat import Message

import logging
logging.basicConfig(level=logging.INFO)
   
with st.spinner("Loading..."):
    os.environ['OPENAI_API_KEY']   = st.secrets.store_api_key.OPENAI_API_KEY
    os.environ['PINECONE_API_KEY'] = st.secrets.store_api_key.PINECONE_API_KEY
    
    index_name = 'dev'
    namespace = 'default'

    pinecone_client = Pinecone()

    assistant = pinecone_client.assistant.Assistant(assistant_name="pdf")

    files = assistant.list_files()
    for file in files:
        if file.name != "Guia - Lya Health.pdf":
            response = assistant.upload_file(
                file_path="pdf/Guia - Lya Health.pdf",
                timeout=None
            )

    files = assistant.list_files()
    for file in files:
        st.write(file.name)

    question = st.text_area(
        "Faça uma pergunta ao assistente.",
        #placeholder="Crie uma tabela com o número do processos, nome do réu, data hora e local, julgamento simplificado em DEFERIDO ou INDEFERIDO.",
        value="O que é tratado no documento ?",
        disabled=False,
    )

    msg = Message(content=question)
    resp = assistant.chat(messages=[msg])

    st.write(resp.message.content)

    # Chat with the assistant.
    #chat_context = [
    #    chat_context = [
    #        Message(content='What is the maximum height of a red pine?', role='user'),
    #        Message(content='The maximum height of a red pine (Pinus resinosa) is up to 25 meters.', role='assistant'),
    #        Message(content='What is its maximum diameter?', role='user')
    #    ]
    #]
    #response = assistant.chat_completions(messages=chat_context)