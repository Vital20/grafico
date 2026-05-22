import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import pandas as pd
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

        # fingir navegador real
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        # acessar site
        response = requests.get(site, headers=headers)

        # transformar html
        soup = BeautifulSoup(response.text, 'html.parser')

        # pegar só manchetes
        titulos = soup.find_all(['h1', 'h2', 'h3'])

        texto = ""

        for titulo in titulos:

            texto += titulo.get_text() + " "

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
            'porque',
            'principal',
            'página',
            'menu',
            'outros'
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

        # tabela
        st.subheader("📊 Top 10 palavras")

        df_top10 = pd.DataFrame(
            top10,
            columns=['Palavra', 'Quantidade']
        )

        st.dataframe(df_top10)

        # separar gráfico
        nomes = []
        valores = []

        for item in top10:

            nomes.append(item[0])

            valores.append(item[1])

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
