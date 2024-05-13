import re #regex işlemleri için
import streamlit as st #gui tasarımı için
import nltk
import webbrowser
nltk.download('stopwords')
nltk.download('punkt')


#NLTK paketleri
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#SPACY paketleri
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

#Function for NLTK
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

    sentence_list= sent_tokenize(docx)
    #sentenceValue = dict()
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
                        sentence_scores[sent] += freqTable[word] #toplamm kelime uzunluğu

    import heapq
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

#Function for SPACY
def spacy_summarizer(docx):
    #nlp=spacy.load('en_core_web_lg')
    #docx=nlp(docx)
    stopWords = list(STOP_WORDS)
    words = word_tokenize(docx)
    freqTable = dict()

    for word in words:
        word = word.lower()
        if word not in stopWords:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(docx)
    #sentenceValue = dict()
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
                        sentence_scores[sent] += freqTable[word]    #Toplam kelime uzunluğuu    

    import heapq
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def main():
    st.title("Metin Özetleme Uygulaması")
    st.subheader("created by: Berktug Berke Ates")
    st.write("Bu uygulama, metin özetleme işlemi yapmaktadır. İki farklı model ile özetleme işlemi yapılmaktadır. NLTK ve SPACY modelleri ile özetleme işlemi yapılmaktadır. Lütfen metni giriniz ve hangi model ile özetleme yapmak istediğinizi seçiniz.")
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
        article_text = st.text_area("Metni giriniz","Buraya yazınız")
        
        #Temizleme işlemi
        article_text = re.sub(r'\\[[0-9]*\\]', ' ',article_text)
        article_text = re.sub('[^a-zA-ZçğİÇĞŞşÖÜöüıİ.,]', ' ', article_text) #regular expression işlemi
        article_text = re.sub(r"\b[a-zA-Z]\b",'',article_text)
        article_text = re.sub("[A-Z]\Z",'',article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        summary_choice = st.selectbox("Özet Seçimi" , ["NLTK","SPACY"])
        if st.button("Metin Yoluyla Özetle"):
            if summary_choice == 'NLTK':
                summary_result = nltk_summarizer(article_text)
            elif summary_choice == 'SPACY':
                summary_result = spacy_summarizer(article_text)

            st.write(summary_result)


if __name__=='__main__':
	main()
