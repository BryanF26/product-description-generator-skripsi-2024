from fastapi import FastAPI
from starlette.responses import Response
# pip install happytransformer
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

app = FastAPI()

@app.post('/generateGPT2')
def generate_gpt2(category: str, title: str, feature: str):
    happy_gen = HappyGeneration(load_path="./GPT 2")
    gen_args = settings()
    text = f"""Categories: {category}
    Title: {title}
    Features: {feature}
    Description: """
    result = happy_gen.generate_text(text, args=gen_args)
    output = result.text
    return output

@app.post('/generateGPTNeo')
def generate_gptneo(category:str, title:str, feature:str):
    happy_gen = HappyGeneration(load_path="./GPT Neo")
    gen_args = settings()
    text = f"""Categories: {category}
    Title: {title}
    Features: {feature}
    Description: """
    result = happy_gen.generate_text(text, args=gen_args)
    output = result.text
    return output