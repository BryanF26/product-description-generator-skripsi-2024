# Product Description Generator
Product Description Generator is a website application using pre-trained models and provide high-quality, varied, and interesting product description using Python, Streamlit, and FastAPI. 
We use Amazon Review Data (2018) and applies **GPT-2**, an advanced language model created by OpenAI that is well-known for its capacity to generate coherent and contextually appropriate text in response to a given prompt. 
In addition, we introduce **GPT-Neo**, an open-source alternative that matches the GPT-3 design. 

There are three main menu that you can explore.
- First is Test model which you can test the model GPT-2 or GPT-Neo and choose description which has been provided using your own parameter.
- Second is Generate to generate product description with your input title and feature using our proposed model GPT-Neo.
- Lastly, you can find your generated text in History.

## Installation
You need to install all required packages which are listed in the *requirements.txt* to run this web app.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required package.

```
pip install -r requirements.txt
```

## Run Application
After installing all the required libraries, you can run this application on your local machine by running this command.
The app is created using streamlit for the frontend and fastapi for the backend.

Create two separate directories for the frontend and backend

To run frontend, run the following command:
`streamlit run Frontend.py`

To run backend, run the following command:
`uvicorn FastApi:app --reload`
