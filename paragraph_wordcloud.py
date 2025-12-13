# -*- coding: utf-8 -*-
"""Paragraph_Wordcloud.ipynb

Original file is located at
    https://colab.research.google.com/drive/1H-y6XMZpOwj05Eky_Y_B55nM2mDwgOin
"""

!pip install streamlit
!pip install pypdf
import streamlit as st
import pypdf
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download("punkt")
nltk.download("stopwords")

st.title("Keyword Paragraph Extractor App")
st.write("Upload a  PDF, Enter Keywords and model will Extract Relevant Paragraphs and form WordCloud")

uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])
keywords = st.text_input("Enter keywords separated by commas", "")

if uploaded_file is not None and keywords:
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + " "

if 'text' in locals() and text:
    clean = re.sub(r'[^a-zA-Z0-9\s.]', " ", text)
    clean = re.sub(r'[0-9]+', "", clean)
    clean = clean.lower()
    clean = re.sub(r'\s+', " ", clean)

    paragraphs = clean.split(".")
    keys = [k.strip().lower() for k in keywords.split(",")]

    extracted = []
    for p in paragraphs:
            if any(k in p for k in keys):
                extracted.append(p.strip())

    st.subheader("Extracted Paragraphs")
    st.write(extracted)

    all_text = " ".join(extracted)
    stop = set(stopwords.words("english"))
    if all_text:
        wc = WordCloud(width=1000, height=500, stopwords=stop).generate(all_text)

        st.subheader("WordCloud from Extracted Paragraphs")
        fig = plt.figure(figsize=(12,5))
        plt.imshow(wc)
        plt.axis("off")
        st.pyplot(fig)
    else:
        st.write("No relevant paragraphs found for the given keywords.")
else:
    st.write("Please upload a PDF and enter keywords to see results.")

