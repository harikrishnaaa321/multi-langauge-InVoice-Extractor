from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image, prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file found")

st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Invoice Extractor Application")

input_text = st.text_input("Input Prompt", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice", type=["jpg", "png", "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    submit = st.button("Tell me about the invoice")

    input_prompt = '''
    You are an expert in understanding invoices. We will upload an image as an invoice and you have to answer any questions based on the uploaded invoice image.
    '''

    if submit:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_text, image_data[0], input_prompt)
        st.subheader("The response is")
        st.write(response)
