import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

url = 'http://127.0.0.1:8000'

tab1, tab2, tab3 = st.tabs(["Information", "Generate","Model"])

with tab1:
    st.title('Introduction')

with tab2:
    st.title('Text Generation Based On GPT')
    models = ['GPT 2', 'GPT Neo']
    selected_model = st.selectbox('Model:', models)

    categories = ['Electronics', 'Home & Kitchen', 'Toys & Games']
    selected_category = st.selectbox('Category:', categories)

    title_input = st.text_input('Title:')

    feature_input = st.text_area('Feature:')

with tab3:
    st.title('Model Details')

def generates(url, selected_category, title_input, feature_input):
    text = requests.post(url,
                        params={
                            'category':selected_category,
                            'title': title_input,
                            'feature': feature_input
                        }
    )
    return text.json()

if st.button('Generate Text'):
    if title_input == "" and feature_input == "":
        st.write(f'Please fill Title and Features')
    else:
        if selected_model == "GPT 2":
            endpoint = '/generateGPT2'
        if selected_model == "GPT Neo":
            endpoint = '/generateGPTNeo'
        generated_text = generates(url+endpoint, selected_category, title_input, feature_input)
        try:
            generated_text = generated_text.split('Description:')[1]
            st.write(f'Generated Description: {generated_text}')
        except:
            st.write(f'Generated Description: {generated_text}')