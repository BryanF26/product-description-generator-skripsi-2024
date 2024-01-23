from fastapi import FastAPI
from happytransformer import HappyGeneration, GENSettings
import nltk
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu
nltk.download('punkt')

data_store = []

data_description = {
    'Electronics':[
        "",
        "",
        ""
    ], 
    'Home & Kitchen':[
        "",
        "",
        ""
    ],
    'Toys & Games':[
        "",
        "",
        ""
    ]
}

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
    return scores['rouge-l']['f']

def calculate_bleu_scores(model_summaries, reference_summaries):
    bleu_scores = []
    for model, reference in zip(model_summaries, reference_summaries):
        model_tokens = nltk.word_tokenize(model)
        reference_tokens = [nltk.word_tokenize(reference)]
        bleu_scores = sentence_bleu(reference_tokens, model_tokens)
    
    return bleu_scores

app = FastAPI()

@app.post('/testGPT2')
def generate_gpt2(category: str, description: str, min_val: int, max_val: int, temps: float, top_ks: int):
    if category == 'Electronics':
        data_electronic
    elif category == 'Home & Kitchen':
        data_home_and_kitchen
    elif category == 'Toys & Games':
        data_toy_and_games
    happy_gen = HappyGeneration(load_path="./GPT 2")
    gen_args = settings(min_val, max_val, temps, top_ks)
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
    bleu_score = calculate_bleu_scores(output,description)
    rouge_score = calculate_rouge_l_f_scores(output, description)
    return output, bleu_score, rouge_score

@app.post('/testGPTNeo')
def generate_gptneo(category: str, description: str, min_val: int, max_val: int, temps: float, top_ks: int):
    if category == 'Electronics':
        data_electronic
    elif category == 'Home & Kitchen':
        data_home_and_kitchen
    elif category == 'Toys & Games':
        data_toy_and_games
    happy_gen = HappyGeneration(load_path="./GPT Neo")
    gen_args = settings(min_val, max_val, temps, top_ks)
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
    bleu_score = calculate_bleu_scores(output,description)
    rouge_score = calculate_rouge_l_f_scores(output, description)
    return bleu_score, rouge_score

@app.post('/generateText')
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

@app.get('/history')
def show_history():
    return data_store

@app.get('/allHistory')
def delete_all_history():
    data_store.clear()