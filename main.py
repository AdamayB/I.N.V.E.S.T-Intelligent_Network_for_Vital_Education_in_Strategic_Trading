import chainlit as cl
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
from langchain.chains import RetrievalQA
from langchain.llms import CTransformers
# Access environment variables
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv('example.env')

huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

#
repo_id = "tiiuae/falcon-7b-instruct"
llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                     repo_id=repo_id,
                     model_kwargs={"temperature":0.6, "max_new_tokens":2000})



template = """
You are an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.

{question}

"""



@cl.on_chat_start
async def start():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)
@cl.on_message
async def main(message):
    llm_chain = cl.user_session.get("llm_chain")
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res["text"]).send()