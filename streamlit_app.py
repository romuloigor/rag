"""Streamlit and OpenAi API."""

import login
import logging
import streamlit as st

from streamlit_oauth import OAuth2Component
from streamlit_cookies_controller import CookieController

st.set_page_config(
    page_title='Seja bem-vindo a CTC Digital!',
    page_icon = 'media/ctc.png',
    layout="wide",
    initial_sidebar_state='collapsed',
    menu_items={
        'Get Help': 'mailto:romulo.conceicao@ctctech.com.br',
        'Report a Bug': "https://github.com/romuloigor/rag/issues",
        'About': "#INOVA.ai"
    }
)

DISABLE_LOGIN = False
st.session_state['DISABLE_LOGIN'] = DISABLE_LOGIN

logging.basicConfig(level=logging.INFO)

controller = CookieController()

paginas = [
    st.Page("pages/vector_store.py", title="Noticias", icon="🗞️")
]

pagina_atual = st.navigation(paginas)
pagina_atual.run()

with st.sidebar:
    st.session_state["login"] = login.login(controller)