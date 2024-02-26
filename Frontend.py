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
    return text

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
            endpoint = '/test/gpt-2'
        if selected_model == "GPT Neo":
            endpoint = '/test/gpt-neo'
        score = test_model(url+endpoint, selected_category, selected_description, min_val, max_val, temps, top_ks)
        evaluation = score.json()
        st.write(f'Generated Description: {evaluation[0]}')
        st.write(f'Generated Bleu Score: {evaluation[1]}')
        st.write(f'Generated Rouge-L Score: {evaluation[2]}')
        st.success('You have success test model')

def generated_text_button():
    if st.button('Generate Text'):
        if title_input == "" or feature_input == "":
            return st.warning(f'Please fill Title and Features')
        generated_text = generates(url+'/generate', selected_category, title_input, feature_input)
        st.write(f'Generated Description: {generated_text}')
        st.success('You have success generate product description')

tab1, tab2, tab3, tab4 = st.tabs(["Home", "Test Model", "Generate","History"])

with tab1:
    st.title('Introduction')
    st.write("Welcome to our website Product Description Generator. Using sophisticated language models, GPT-2 and GPT-Neo, we provide a breakthrough tool for creating high-quality, varied, and interesting writing.")
    st.write("We use GPT-2, an advanced language model created by OpenAI that is well-known for its capacity to generate coherent and contextually appropriate text in response to a given prompt. In addition, we introduce GPT-Neo, an open-source alternative that matches the GPT-3 design.")
    st.write("There are three main menu that you can explore. First is Test model which you can test the model GPT-2 or GPT-Neo and choose description which has been provided using your own parameter. Second is Generate to generate product description with your input title and feature using our proposed model GPT-Neo. Lastly, you can find your generated text in History.") 

with tab2:
    st.title('Testing Model')
    
    models = ['GPT 2', 'GPT Neo']
    selected_model = st.selectbox('Model:', models, key="model")
    
    categories = ['Electronics', 'Home & Kitchen', 'Toys & Games']
    selected_category = st.selectbox('Category:', categories, key="category")
    
    description = requests.get(url+'/description').json()
    selected_description = st.selectbox('Description:', options=[d["description"] for d in description[selected_category]], key="description")
    
    min_val = st.slider('Min (Minimal Length Generate)', min_value=10, max_value=100, value=10)
    max_val = st.slider('Max (Maximal Length Generate)', min_value=10, max_value=100, value=50)
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
        requests.delete(url+'/history')
        st.success('You have success delete history')