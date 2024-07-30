from langchain.document_loaders import HuggingFaceDatasetLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import AutoTokenizer, pipeline
from langchain import HuggingFacePipeline
from langchain.chains import RetrievalQA

from datasets import load_dataset
import requests
from get_yaml import get_prompt

'''
Summarize the content with retriever and generate the topic with LLM
'''


def content2topic(content):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)

    docs = text_splitter.create_documents([content])

    # Define the path to the pre-trained model you want to use
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {'device': 'cpu'}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,  # Provide the pre-trained model's path
        model_kwargs=model_kwargs,  # Pass the model configuration options
        encode_kwargs=encode_kwargs  # Pass the encoding options
    )

    db = FAISS.from_documents(docs, embeddings)

    questions = ["What are the new concepts, methods or techniques presented in the paper?",
                 "What are the main contributions of the paper in this research area, specifically?",
                 "What specific problems did the paper address and what solutions did it propose?",
                 "What are the main results and findings of the experiments or data analyzed in the paper?",
                 "What are the main research methods and techniques used in the paper?",
                 "What are the potential application scenarios and practical implications of the research results?",
                 "How does this paper's work compare to and improve upon previous research?"]

    answers = set()

    for question in questions:
        searchDocs = db.similarity_search(question)
        answers.add(searchDocs[0].page_content)
        answers.add(searchDocs[1].page_content)
        answers.add(searchDocs[2].page_content)

    # LLM module

    context = "\n".join(answers)

    question = get_prompt("retriever")

    content = context + "\n\n" + question

    # print(content)

    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "Qwen/Qwen2-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer sk-qwiklihnbaklwmpmnqdthifvpbbgctfvfubokpucoirblvio"
        # Replace your_token with your actual token
    }

    response = requests.post(url, json=payload, headers=headers)

    response_json = response.json()
    llm_reply = response_json.get("choices")[0].get("message").get("content")
    # print(llm_reply)
    
    return llm_reply