import streamlit as st
import PyPDF2
import tempfile
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration

# Function to extract text from PDF document


def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(pdf_file.read())
        tmp.seek(0)
        pdf_reader = PyPDF2.PdfReader(tmp)
        page_count = list(pdf_reader.pages())
        text = ''

        for page in page_count:
            text += page.extractText()
            return text
# Function to summarize text using T5 model


def t5_summarize(text):
    model = T5ForConditionalGeneration.from_pretrained('t5-base')
    tokenizer = T5Tokenizer.from_pretrained('t5-base', model_max_length=1024)
    input_ids = tokenizer.encode("summarize: " + text, return_tensors='pt')
    output = model.generate(input_ids=input_ids,
                            max_length=150, num_beams=2, early_stopping=True)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary

# Function to summarize text using Bart model


def bart_summarize(text):
    model = BartForConditionalGeneration.from_pretrained(
        'facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    input_ids = tokenizer.encode(text, return_tensors='pt')
    output = model.generate(input_ids=input_ids,
                            max_length=150, num_beams=2, early_stopping=True)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary


# Streamlit app code
st.title("Research Paper Summarizer")

pdf_file = st.file_uploader("Upload PDF file", type="pdf")
if pdf_file:
    text = extract_text_from_pdf(pdf_file)
    st.write("**Original text:**")
    st.write(text)

    st.write("**T5 Summary:**")
    t5_summary = t5_summarize(text)
    st.write(t5_summary)

    st.write("**BART Summary:**")
    bart_summary = bart_summarize(text)
    st.write(bart_summary)
