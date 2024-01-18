from happytransformer import HappyGeneration, GENSettings

def settings():
    min_length =  50
    max_length = 100 
    do_sample = True
    early_stopping = True
    num_beams = 1 
    temperature = 0.7
    top_k = 50
    top_p = 0.7
    no_repeat_ngram_size = 2
    gen_args = GENSettings(min_length, max_length, do_sample, early_stopping, num_beams, temperature, top_k, no_repeat_ngram_size, top_p)
    return gen_args

def generate_gpt2(category, title, feature):
    happy_gen = HappyGeneration(load_path="./GPT 2")
    gen_args = settings()
    text = f"""Categories: {category}
    Title: {title}
    Features: {feature}
    Description: """
    result = happy_gen.generate_text(text, args=gen_args)
    output = result.text.split("Description: ")[1]
    return  output

import streamlit as st

url = 'http://localhost:8501'

st.title('Text Generation Based On GPT')

models = ['GPT 2', 'GPT Neo']
selected_model = st.selectbox('Model:', models)

categories = ['Electronics', 'Home & Kitchen', 'Toys & Games']
selected_category = st.selectbox('Category:', categories)

title_input = st.text_input('Title:')

feature_input = st.text_area('Feature:')

if st.button('Generate Text'):
    if title_input == "" and feature_input == "":
        st.write(f'Please fill Title and Features')
    else:
        if selected_model == "GPT 2":
            endpoint = '/generateGPT2'
        if selected_model == "GPT Neo":
            endpoint = '/generateGPTNeo'
        generated_text = generate_gpt2(selected_category, title_input, feature_input)
        st.write(f'Generated Description: {generated_text}')
        