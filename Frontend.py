import streamlit as st
import requests
import pandas as pd

url = 'http://127.0.0.1:8000'

def test_model(url, selected_category, selected_description, min_val, max_val, temps, top_ks):
    text = requests.post(url,
                        params={
                            'category':selected_category,
                            'description': selected_description,
                            'min_val': min_val,
                            'max_val': max_val,
                            'temps': temps,
                            'top_ks': top_ks
                        }
    )
    return text.json()

def generates(url, selected_category, title_input, feature_input):
    text = requests.post(url,
                        params={
                            'category':selected_category,
                            'title': title_input,
                            'feature': feature_input,
                        }
    )
    return text.json()


def test_model_button():
    if st.button('Test Model'):
        if selected_model == "GPT 2":
            endpoint = '/testGPT2'
        if selected_model == "GPT Neo":
            endpoint = '/testGPTNeo'
        bleu_score, rouge_score = test_model(url+endpoint, selected_category, selected_description, min_val, max_val, temps, top_ks)
        st.write(f'Generated Bleu Score: {bleu_score}')
        st.write(f'Generated Rouge-L Score: {rouge_score}')

def generated_text_button():
    if st.button('Generate Text'):
        if title_input == "" or feature_input == "":
            return st.write(f'Please fill Title and Features')
        generated_text = generates(url+'/generateText', selected_category, title_input, feature_input)
        st.write(f'Generated Description: {generated_text}')


tab1, tab2, tab3, tab4 = st.tabs(["Home", "Test Model", "Generate","History"])

with tab1:
    st.title('Introduction')
    st.write("Welcome to our revolutionary website, where the cutting edge of AI-powered creativity meets the ever-changing demands of digital content. Using sophisticated language models, GPT-2 and GPT-Neo, we provide a breakthrough tool for creating high-quality, varied, and interesting writing.")
    st.write("Our platform is based on the idea of improving human creativity with AI support. Whether you're a marketing searching for compelling product descriptions, our service meets a wide range of text generating of product description.")
    st.write("We use GPT-2, an advanced language model created by OpenAI that is well-known for its capacity to generate coherent and contextually appropriate text in response to a given prompt. In addition, we introduce GPT-Neo, an open-source alternative that matches the GPT-3 design.")
    st.write("Our user-friendly interface allows you to easily choose model and category you want and input your product title and feature. With a few clicks, you can produce product description as the outcome.")    
    
with tab2:
    st.title('Testing Model')
    
    models = ['GPT 2', 'GPT Neo']
    selected_model = st.selectbox('Model:', models, key="model")
    
    categories = ['Electronics', 'Home & Kitchen', 'Toys & Games']
    selected_category = st.selectbox('Category:', categories, key="category")
    
    description = requests.get(url+'/description').json()
    selected_description = st.selectbox('Description:', options=[d for d in description[categories]], key="description")
    
    min_val = st.slider('Temperature (Unique Word Generate)', min_value=10, max_value=100, value=10)
    max_val = st.slider('Temperature (Unique Word Generate)', min_value=10, max_value=100, value=50)
    temps = st.slider('Temperature (Unique Word Generate)', min_value=0.1, max_value=1.0, value=0.7)
    top_ks = st.slider('Top_K (Possiblity Word Generate)', min_value=0, max_value=100, value=50)
    
    test_model_button()
    
    
with tab3:
    st.expander('Generate',False)
    st.title('Text Generation')
    categories = ['Electronics', 'Home & Kitchen', 'Toys & Games']
    selected_category = st.selectbox('Category:', categories)
    title_input = st.text_input('Title:')
    feature_input = st.text_area('Feature:')
    generated_text_button()

with tab4:
    st.title('History')
    data = []
    data = requests.get(url+'/history').json()
    df = pd.DataFrame(data,columns=['Category', 'Title', 'Feature', 'Description'])
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button('Clear History'):
        requests.get(url+'/allHistory').json()
        st.rerun()