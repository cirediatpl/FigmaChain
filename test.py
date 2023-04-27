### import os

# Load necessary libraries for chat, file processing and text manipulation
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

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Setup FigmaFileLoader object with necessary tokens and keys
figma_loader = FigmaFileLoader(
    os.environ.get('ACCESS_TOKEN'),
    os.environ.get('NODE_IDS'),
    os.environ.get('FILE_KEY'),
)

# Create the searchable vectorstore index with the Figma loader
index = VectorstoreIndexCreator().from_loaders([figma_loader])

# Create retriever for Figma document nodes
figma_doc_retreiver = index.vectorestore.as_retriever()

def generate_code(input):
    # Define system prompt template for AI model
    system_prompt_template = """You are an expert coder and developer.

    Use the provided design context to create idiomatic HTML/CSS code based on the user request.

    Everything must be inline in one file and your response must be directly renderable by the browser.

    Figma file nodes and metadata: {context}"""

    # Define human prompt template for AI model
    human_prompt_template = "Code the {text}. Ensure it's mobile responsive."

    # Create prompts from templates
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template)

    # Setup AI chat model (GPT-4) with temperature and model_name
    gpt_4 = ChatOpenAI(temperature=.02, model_name='gpt-4')

    # Retrieve relevant Figma nodes for the input text
    relevant_nodes = figma_doc_retreiver.get_relevant_documents(input)

    # Create chat prompt with context
    conversation = ChatPromptTemplate.create_promise_from_nodes(relevant_nodes)

    # Add initial system message to the conversation
    conversation = conversation.join("system", system_message_prompt)

    # Add human message to the conversation
    conversation = conversation.join("human", human_message_prompt.formatted(text=input))

    # Create conversation buffer and chain for AI response
    conversation_memory = ConversationBufferWindowMemory()
    conversation_chain = LLMChain(gpt_4, conversation_memory)

    # Get AI response as code
    response = conversation_chain.respond(conversation)
    code = response['choices'][0]['text']

    return code

    # Read input from user

user_input = "Create a simple navigation bar"

    # Generate the code based on the user input

generated_code = generate_code(user_input)
print(generated_code)