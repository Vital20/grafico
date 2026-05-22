import streamlit as st
from docling.document_converter import DocumentConverter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re

# baixar stopwords
nltk.download('stopwords')

# título do site
st.title("Analisador de Manchetes de Futebol")

# input do usuário
site = st.text_input(
    "Digite o site:",
    "https://ge.globo.com/futebol/"
)

# botão
if st.button("Analisar site"):

    st.write("Lendo o site...")

    # converter site em texto
    converter = DocumentConverter()
    doc = converter.convert(site).document

    texto = doc.export_to_markdown()

    # limpeza do texto
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
        'horas'
    ]

    stop_words.update(extras)

    # separar palavras
    palavras = texto.split()

    palavras_filtradas = []

    for palavra in palavras:
        if palavra not in stop_words and len(palavra) > 3:
            palavras_filtradas.append(palavra)

    # contagem
    contagem = Counter(palavras_filtradas)

    # top 10
    top10 = contagem.most_common(10)

    nomes = []
    valores = []

    for item in top10:
        nomes.append(item[0])
        valores.append(item[1])

    # mostrar tabela
    st.subheader("Top 10 palavras")

    st.write(top10)

    # gráfico
    st.subheader("Gráfico")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(nomes, valores)

    ax.set_title("Palavras mais frequentes")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    # nuvem de palavras
    st.subheader("Nuvem de palavras")

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        min_font_size=10
    ).generate_from_frequencies(contagem)

    fig2, ax2 = plt.subplots(figsize=(15,7))

    ax2.imshow(wordcloud)

    ax2.axis('off')

    st.pyplot(fig2)
