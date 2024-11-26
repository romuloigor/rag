"""Streamlit and OpenAi API."""

import logging
import os
import streamlit as st
import pandas as pd
from datetime import datetime

from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

logging.basicConfig(level=logging.INFO)

from openai import OpenAI

if 'login' in st.session_state:
    if ( st.session_state['login'] and ( "auth" in st.session_state ) ) or st.session_state.DISABLE_LOGIN:
        client = OpenAI(api_key=st.secrets.store_api_key.OPENAI_API_KEY)

        if st.button('List vector'):
            vector_stores = client.beta.vector_stores.list()
            id = 1
            for item in vector_stores.data:
                
                row = {
                    'id': 1,
                    'vec_id': item.id,
                    'vec_name': item.name,
                    'vec_usage_bytes': item.usage_bytes,
                    #'file_counts': item.file_counts,
                    'vec_last_active_at': datetime.fromtimestamp(item.last_active_at).strftime('%d/%m/%Y %H:%M:%S')
                }

                id =+ 1

                #st.write(row)
                st.json(row)

                df = pd.DataFrame([row])
                
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "vec_id": "vector id",
                        "vec_usage_bytes": st.column_config.NumberColumn(
                            "usage_bytes",
                            help="Bytes usage?",
                            min_value=1000,
                            max_value=10000,
                            step=1,
                            format="%d ⭐",
                        ),
                        "vector_name": "Widget ?",
                    },
                    disabled=["vector_name"],
                    hide_index=True,
                )

        del_vector_id = st.text_input('Delete vector id:')
        if st.button('Delete vector'):
            deleted_vector_store = client.beta.vector_stores.delete(
                vector_store_id=del_vector_id
            )
            st.write(deleted_vector_store)

        vector_name = st.text_input('Create vector name:')
        if st.button('Create vector'):
            vector_store = client.beta.vector_stores.create(name=vector_name)
            st.write(vector_store)

        if st.button('List vector files'):
            vector_store_files = client.beta.vector_stores.files.list(
                vector_store_id="vs_qg8gwFYbdhfsJMqwXhfTYJXt"
            )
            st.write(vector_store_files.data[0])

        if st.button('Send pdf'):
            pdf_file = st.file_uploader("Send PDF", type="pdf")
            if pdf_file is not None:
                response = client.files.create(
                    file=pdf_file,
                    purpose='user_data'
                )
                st.write(response)

        if st.button('Store pdf in vector'):
            vector_store_file = client.beta.vector_stores.files.create(
                vector_store_id="vs_qg8gwFYbdhfsJMqwXhfTYJXt",
                file_id="file-KQGRvxUQ3Rny3WQtcMWDxZ"
            )
            st.write(vector_store_file)

        if st.button('Status store pdf in vector'):
            vector_store_file = client.beta.vector_stores.files.retrieve(
                vector_store_id="vs_qg8gwFYbdhfsJMqwXhfTYJXt",
                file_id="file-KQGRvxUQ3Rny3WQtcMWDxZ"
            )
            st.write(vector_store_file)

        if st.button('Create Assistant'):
            consulta = "O que se trata no documento?"

            assistant = client.beta.assistants.create(
                name="Assistant",
                model="gpt-4o",
                tools=[{"type": "file_search"}],
                tool_resources={"file_search": {"vector_store_ids": ['vs_qg8gwFYbdhfsJMqwXhfTYJXt']}}
            )

            # Crie um thread e execute a busca
            thread = client.beta.threads.create(
                messages=[{"role": "user", "content": consulta}]
            )
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id
            )

            # Obtenha e exiba os resultados
            messages = client.beta.threads.messages.list(thread.id)
            resposta = messages.data[0].content[0]
            if resposta.type == 'text':
                st.write("Resposta:", resposta.text.value)
                st.write("Anotações:", resposta.text.annotations)

        if st.button('List Assistant'):
            resposta = client.beta.assistants.list()
            st.write(resposta.data)