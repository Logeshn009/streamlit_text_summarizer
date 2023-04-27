import torch
import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration
from db_connection import db


@st.cache_data
def run_model(model, _num_beams, _no_repeat_ngram_size, _length_penalty, _min_length, _max_length, _early_stopping, text, user_name):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if model == "BART":

        # Load the BART tokenizer and model
        bart_model = BartForConditionalGeneration.from_pretrained(
            "facebook/bart-large-cnn")
        bart_tokenizer = BartTokenizer.from_pretrained(
            "facebook/bart-large-cnn")

        # Define the input text to summarize
        input_text_ = str(text)
        input_text = ' '.join(input_text_.split())
        input_tokenized = bart_tokenizer.encode(
            input_text, return_tensors='pt').to(device)

        # Generate the summary
        summary_ids = bart_model.generate(input_tokenized,
                                          num_beams=_num_beams,
                                          no_repeat_ngram_size=_no_repeat_ngram_size,
                                          length_penalty=_length_penalty,
                                          min_length=_min_length,
                                          max_length=_max_length,
                                          early_stopping=_early_stopping)

        output = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in
                  summary_ids]

        data_bart = {"username": user_name,
                     "model": model,
                     "parameters":
                         {"_num_beams": _num_beams,
                          "_no_repeat_ngram_size": _no_repeat_ngram_size,
                          "_length_penalty": _length_penalty,
                          "_min_length": _min_length,
                          "_max_length": _max_length,
                          "_early_stopping": _early_stopping},
                     "summarized_text":
                         {"input_text": text,
                          "summarized_text": output}}
        db.summarized_text.insert_one(data_bart)
        # print(data_bart)
        st.subheader("Summarized text")
        st.success(output[0])
        return data_bart

    else:
        t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
        t5_tokenizer = T5Tokenizer.from_pretrained(
            "t5-base", model_max_length=1024)
        input_text_ = str(text).replace('\n', '')
        input_text = ' '.join(input_text_.split())
        input_tokenized = t5_tokenizer.encode(
            input_text, return_tensors="pt").to(device)
        summary_task = torch.tensor([[21603, 10]]).to(device)
        input_tokenized = torch.cat(
            [summary_task, input_tokenized], dim=-1).to(device)
        summary_ids = t5_model.generate(input_tokenized,
                                        num_beams=_num_beams,
                                        no_repeat_ngram_size=_no_repeat_ngram_size,
                                        length_penalty=_length_penalty,
                                        min_length=_min_length,
                                        max_length=_max_length,
                                        early_stopping=_early_stopping)
        output = [t5_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in
                  summary_ids]
        data_t5 = {"username": user_name,
                   "model": "T5",
                   "parameters":
                       {"_num_beams": _num_beams,
                        "_no_repeat_ngram_size": _no_repeat_ngram_size,
                        "_length_penalty": _length_penalty,
                        "_min_length": _min_length,
                        "_max_length": _max_length,
                        "_early_stopping": _early_stopping},
                   "summarized_text":
                   {"input_text": text,
                           "output_text": output}
                   }
        db.summarized_text.insert_one(data_t5)
        # print(data_t5)
        st.subheader("Summarized text")
        st.success(output[0])
        return data_t5


def text_summarizer_ui():
    user_name = st.session_state["user_name"]
    # st.write(user_name)
    st.title('Text Summarizer for Researchers')
    st.divider()
    st.header('Using BART and T5 transformer model')
    st.subheader('Select Model')
    model = st.selectbox('', ('BART', 'T5'))
    st.subheader('Set Parameters')
    if model == 'BART':
        _num_beams = 4
        _no_repeat_ngram_size = 3
        _length_penalty = 1
        _min_length = 12
        _max_length = 128
        _early_stopping = True
    else:
        _num_beams = 4
        _no_repeat_ngram_size = 3
        _length_penalty = 2
        _min_length = 30
        _max_length = 200
        _early_stopping = True

    col1, col2, col3 = st.columns(3)
    _num_beams = col1.number_input("num_beams", value=_num_beams)
    _no_repeat_ngram_size = col2.number_input(
        "no_repeat_ngram_size", value=_no_repeat_ngram_size)
    _length_penalty = col3.number_input(
        "length_penalty", value=_length_penalty)

    col1, col2, col3 = st.columns(3)
    _min_length = col1.number_input("min_length", value=_min_length)
    _max_length = col2.number_input("max_length", value=_max_length)
    _early_stopping = col3.number_input(
        "early_stopping", value=_early_stopping)
    st.divider()
    st.subheader("Text Input")
    text = st.text_area(
        '', height=300, placeholder="Paste your input text here to start summarizing    ...")

    return (model, _num_beams, _no_repeat_ngram_size, _length_penalty, _min_length, _max_length, _early_stopping, text, user_name)


def call_text_summarizer():

    # Call the UI function and store the return values in variables
    model, num_beams, no_repeat_ngram_size, length_penalty, min_length, max_length, early_stopping, text, user_name = text_summarizer_ui()

    if st.button('Submit'):
        # Call your text summarizer function with the UI parameters as arguments
        run_model(model, num_beams, no_repeat_ngram_size,
                  length_penalty, min_length, max_length, early_stopping, text, user_name)
        # st.write(summary)
