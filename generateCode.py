import os

from langchain.document_loaders.figma import FigmaFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from dotenv import load_dotenv
load_dotenv()

figma_loader = FigmaFileLoader(
    os.environ.get('ACCESS_TOKEN'),
    os.environ.get('NODE_IDS'),
    os.environ.get('FILE_KEY'),
)

index = VectorstoreIndexCreator().from_loaders([figma_loader])
figma_doc_retreiver = index.vectorstore.as_retriever()

def generate_code(input):
    system_prompt_template = """You are an expert coder and developer.

    Use the provided design context to create idiomatic HTML/CSS code based on the user request.

    Everything must be inline in one file and your response must be directly renderable by the browser.

    Figma file nodes and metadata: {context}"""

    human_prompt_template = "Code the {text}. Ensure it's mobile responsive."

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template)
    gpt_4 = ChatOpenAI(temperature=.02, model_name='gpt-4')

    # Use the retreiver's 'get_relevant_documents' method if needed to filter down longer docs

    relevant_nodes = figma_doc_retreiver.get_relevant_documents(input)
    conversation=[system_message_prompt, human_message_prompt]
    chat_prompt = ChatPromptTemplate.from_messages (conversation)
    response = gpt_4(chat_prompt.format_prompt(
        context=relevant_nodes,
        text=input).to_messages())
    return response

response = generate_code("data visualization")