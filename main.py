import streamlit as st
#from streamlit_option_menu import option_menu # Você pode instalar essa biblioteca para personalizar ainda mais
from pages import pesquisa, sobre # Importe as páginas criadas na pasta 'pages'

import sys
import os
sys.path.append(os.path.dirname(__file__))


# Define o layout da página principal usando o Streamlit
st.set_page_config(page_title="Navegação Personalizada", layout="wide")

# Define a navegação com a barra lateral
selected = st.sidebar.selectbox("Selecione a página", ["Página Principal", "Pesquisa", "Sobre"])

# Exibe o conteúdo da página selecionada
if selected == "Página Principal":
    st.title("Página Principal")
    st.write("Bem-vindo à página principal!")
elif selected == "Pesquisa":
    pesquisa.main() # Chama a função 'main' dentro do arquivo 'usuarios.py'
elif selected == "Sobre":
    sobre.main() # Chama a função 'main' dentro do arquivo 'sobre.py'
    
    