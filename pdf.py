from transformers import pipeline
from pdfminer.high_level import extract_text
import docx2txt

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
