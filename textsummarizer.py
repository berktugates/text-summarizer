import re
import streamlit as st
import nltk
import webbrowser
from rouge_score import rouge_scorer

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Function for NLTK Summarization
def nltk_summarizer(docx):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(docx)
    freqTable = dict()

    for word in words:
        word = word.lower()
        if word not in stopWords:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    sentence_list = sent_tokenize(docx)
    max_freq = max(freqTable.values())
    for word in freqTable.keys():
        freqTable[word] = (freqTable[word]/max_freq)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freqTable.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = freqTable[word]
                    else:
                        sentence_scores[sent] += freqTable[word]

    import heapq
    summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

# Function to evaluate summary with ROUGE metrics
def evaluate_summary(reference_summary, generated_summary):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_summary, generated_summary)
    return scores

def main():
    st.title("Metin Özetleme Uygulaması")
    st.subheader("created by: Berktug Berke Ates")
    st.write("Bu uygulama, metin özetleme işlemi yapmaktadır. NLTK modeli ile özetleme işlemi yapılmaktadır. Lütfen metni giriniz.")
    github = st.button("Visit my GitHub")

    if github:
        webbrowser.open("https://github.com/berktugates")

    linkedin = st.button("Visit my LinkedIn")

    if linkedin:
        webbrowser.open("https://www.linkedin.com/in/berktugates/")

    activities = ["Summarize Via Text"]
    choice = st.sidebar.selectbox("İşlemi seçiniz:", activities)

    if choice == 'Summarize Via Text':
        st.subheader("NLP kullanarak metin özetleme işlemi yapınız.")
        
        article_text = st.text_area("Metni giriniz", height=300)
        reference_summary = st.text_area("İsteğe bağlı: Referans Özeti giriniz", height=100)
        
        # Temizleme işlemi
        article_text = re.sub(r'\\[[0-9]*\\]', ' ', article_text)
        article_text = re.sub('[^a-zA-ZçğİÇĞŞşÖÜöüıİ.,]', ' ', article_text)
        article_text = re.sub(r"\b[a-zA-Z]\b", '', article_text)
        article_text = re.sub("[A-Z]\Z", '', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        summary_choice = st.selectbox("Özet Seçimi", ["NLTK"])
        if st.button("Metin Yoluyla Özetle"):
            if summary_choice == 'NLTK':
                summary_result = nltk_summarizer(article_text)
                st.write("Oluşturulan Özet:")
                st.write(summary_result)

                if reference_summary:
                    scores = evaluate_summary(reference_summary, summary_result)
                    st.write("ROUGE Skorları:")
                    st.write(f"ROUGE-1: {scores['rouge1']}")
                    st.write(f"ROUGE-2: {scores['rouge2']}")
                    st.write(f"ROUGE-L: {scores['rougeL']}")

if __name__ == '__main__':
    main()
