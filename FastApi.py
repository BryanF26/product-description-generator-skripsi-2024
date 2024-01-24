from fastapi import FastAPI
from happytransformer import HappyGeneration, GENSettings
import nltk
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu
nltk.download('punkt')
import json
f = open('Data.json')
data_product = json.load(f)
f.close()

data_store = []

def settings(min_val= 50, max_val=100, temp=0.7, top_ks=50):
    min_length =  min_val
    max_length = max_val
    do_sample = True
    early_stopping = True
    num_beams = 1 
    temperature = temp
    top_k = top_ks
    top_p = temp
    no_repeat_ngram_size = 2
    gen_args = GENSettings(min_length, max_length, do_sample, early_stopping, num_beams, temperature, top_k, no_repeat_ngram_size, top_p)
    return gen_args

def calculate_rouge_l_f_scores(model_summaries, reference_summaries):
    rouge = Rouge()
    scores = rouge.get_scores(model_summaries, reference_summaries)
    return scores[0]["rouge-l"]["f"]

def calculate_bleu_scores(models, references):
    model_tokens = nltk.word_tokenize(models)
    reference_tokens = [nltk.word_tokenize(references)]
    bleu_scores = sentence_bleu(reference_tokens, model_tokens)
    return bleu_scores

def get_data(category, description):
    for i in data_product[category]:
        if i['description'] == description:
            return i

app = FastAPI()

@app.post('/test/gpt-2')
def generate_gpt2(category: str, description: str, min_val: int, max_val: int, temps: float, top_ks: int):
    product = get_data(category, description)
    happy_gen = HappyGeneration(load_path="./GPT 2")
    gen_args = settings(min_val, max_val, temps, top_ks)
    descs = product['description'].split(' ')
    text = f"""Categories: {category}
    Title: {product['title']}
    Features: {product['feature']}
    Description: {descs[0]} {descs[1]}"""
    result = happy_gen.generate_text(text, args=gen_args)
    output = result.text
    try:
        output = output.split('Description:')[1]
    except:
        output = output
    bleu_score = calculate_bleu_scores(output, description)
    rouge_score = calculate_rouge_l_f_scores(output, description)
    texts = [output, bleu_score, rouge_score]
    return texts

@app.post('/test/gpt-neo')
def generate_gptneo(category: str, description: str, min_val: int, max_val: int, temps: float, top_ks: int):
    product = get_data(category, description)
    happy_gen = HappyGeneration(load_path="./GPT Neo")
    gen_args = settings(min_val, max_val, temps, top_ks)
    descs = product['description'].split(' ')
    text = f"""Categories: {category}
    Title: {product['title']}
    Features: {product['feature']}
    Description: {descs[0]} {descs[1]}"""
    result = happy_gen.generate_text(text, args=gen_args)
    output = result.text
    try:
        output = output.split('Description:')[1]
    except:
        output = output
    bleu_scoree = calculate_bleu_scores(output, description)
    rouge_score = calculate_rouge_l_f_scores(output, description)
    texts = [output, bleu_scoree, rouge_score]
    return texts

@app.post('/generate')
def generate_gpt2(category: str, title: str, feature: str):
    happy_gen = HappyGeneration(load_path="./GPT Neo")
    gen_args = settings()
    text = f"""Categories: {category}
    Title: {title}
    Features: {feature}
    Description: """
    result = happy_gen.generate_text(text, args=gen_args)
    output = result.text
    try:
        output = output.split('Description:')[1]
    except:
        output = output
    data = [category, title, feature, output]
    data_store.append(data)
    return output

@app.get('/description')
def show_description():
    return data_product

@app.get('/history')
def show_history():
    return data_store

@app.delete('/history')
def delete_all_history():
    data_store.clear()