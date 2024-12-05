"""Streamlit and OpenAi API."""

import login
import logging

from st_on_hover_tabs import on_hover_tabs
import streamlit as st

from streamlit_oauth import OAuth2Component
from streamlit_cookies_controller import CookieController

st.set_page_config(
    page_title='Seja bem-vindo a CTC Digital!',
    page_icon = 'media/ctc.png',
    layout="wide",
    #initial_sidebar_state='collapsed',
    #menu_items={
    #    'Get Help': 'mailto:romulo.conceicao@ctctech.com.br',
    #    'Report a Bug': "https://github.com/romuloigor/rag/issues",
    #    'About': "#INOVA.ai"
    #}
)

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

DISABLE_LOGIN = True
st.session_state['DISABLE_LOGIN'] = DISABLE_LOGIN

logging.basicConfig(level=logging.INFO)

controller = CookieController()

paginas = [
    st.Page("pages/vector_store.py", title="Dashboard", icon="🗞️")
]

pagina_atual = st.navigation(paginas)

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Login','Dashboard'], 
                         iconName=['login','dashboard'], default_choice=0)
    
if tabs == 'Login':
    st.session_state["login"] = login.login(controller)

elif tabs =='Dashboard':
    pagina_atual.run()