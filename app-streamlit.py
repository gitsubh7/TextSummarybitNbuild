from flask import Flask, render_template, request, jsonify
from flask_ngrok import run_with_ngrok
from io import BytesIO
from PyPDF2 import PdfReader
import google.generativeai as palm
import streamlit as st
app = Flask(__name__)
# run_with_ngrok(app)

palm.configure(api_key='AIzaSyATloJFmBEnswSVQf1oOMA3L5F3azDztCE')


def process_pdf(pdf_data):
    if pdf_data:
        reader = PdfReader(BytesIO(pdf_data))
        txt = ""
        summary = ""
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            txt = page.extract_text()
            pt = 'Generate the summary of the following text in atleast 100 words and suggest health precautions that patient should change\n' + txt
            response = palm.generate_text(prompt=pt)
            print(f"{response.result}\n\n")
            if response.result:
                summary += response.result + "\n\n"
        # print(txt)
        if summary != "":
            return summary

    return 'Failed to process the PDF'

def main():
    summary = "Error"
    file = st.file_uploader("Choose a file", type = "pdf")
    if st.button("Predict"):
        if file:
            summary = process_pdf(pdf_data=file.getvalue())
            st.success('The output is {}'.format(summary))





if __name__ == '__main__':
    main()
