import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re

# baixar stopwords
nltk.download('stopwords')

# título
st.title("⚽ Analisador de Manchetes de Futebol")

# descrição
st.write("Cole o link de um site de futebol e veja as palavras mais usadas.")

# input
site = st.text_input(
    "Digite o link do site:",
    "https://ge.globo.com/futebol/"
)

# botão
if st.button("Analisar Site"):

    try:

        st.write("Lendo o site...")

        # acessar site
        response = requests.get(site)

        # transformar html
        soup = BeautifulSoup(response.text, 'html.parser')

        # pegar texto
        texto = soup.get_text()

        # limpar texto
        texto = texto.lower()

        texto = re.sub(r'[^\w\s]', '', texto)

        texto = re.sub(r'\d+', '', texto)

        # stopwords
        stop_words = set(stopwords.words('portuguese'))

        extras = [
            'image',
            'imagem',
            'globo',
            'ge',
            'sportv',
            'facebook',
            'twitter',
            'instagram',
            'youtube',
            'whatsapp',
            'site',
            'seguir',
            'compartilhar',
            'horas',
            'mais',
            'sobre',
            'todos',
            'ainda',
            'porque'
        ]

        stop_words.update(extras)

        # separar palavras
        palavras = texto.split()

        palavras_filtradas = []

        for palavra in palavras:

            if palavra not in stop_words and len(palavra) > 3:

                palavras_filtradas.append(palavra)

        # contar palavras
        contagem = Counter(palavras_filtradas)

        # top 10
        top10 = contagem.most_common(10)

        nomes = []
        valores = []

        for item in top10:

            nomes.append(item[0])

            valores.append(item[1])

        # mostrar top 10
        st.subheader("📊 Top 10 palavras")

        st.write(top10)

        # gráfico
        st.subheader("📈 Gráfico")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(nomes, valores)

        ax.set_title("Palavras mais frequentes")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        # nuvem de palavras
        st.subheader("☁️ Nuvem de Palavras")

        wordcloud = WordCloud(
            width=1000,
            height=500,
            background_color='white'
        ).generate_from_frequencies(contagem)

        fig2, ax2 = plt.subplots(figsize=(15, 7))

        ax2.imshow(wordcloud)

        ax2.axis('off')

        st.pyplot(fig2)

    except Exception as erro:

        st.error(f"Erro ao analisar o site: {erro}")
