import os
import webbrowser
import argparse
from langchain.document_loaders.figma import FigmaFileLoader
from langchain.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the FigmaFileLoader with environment variables
figma_loader = FigmaFileLoader(
    os.environ.get('ACCESS_TOKEN'),
    os.environ.get('NODE_IDS'),
    os.environ.get('FILE_KEY'),
)

# Create an index and retriever for Figma documents
index = VectorstoreIndexCreator().from_loaders([figma_loader])
figma_doc_retreiver = index.vectorstore.as_retriever()

# Define system and human prompt templates
system_prompt_template = """You are a senior developer.
Use the provided design context to create idiomatic HTML/CSS code based on the user request.
Everything must be inline in one file and your response must be directly renderable by the browser.
Write code that matches the Figma file nodes and metadata as exactly as you can.
Figma file nodes and metadata: {context}"""

human_prompt_template = "Code the {text}. Ensure that the code is mobile responsive and follows modern design principles."

# Initialize the ChatOpenAI model
gpt_4 = ChatOpenAI(temperature=.03, model_name='gpt-3.5-turbo', request_timeout=120)

# Define a function to generate code based on the input
def generate_code(input):
    # Get relevant nodes from the Figma document retriever
    relevant_nodes = figma_doc_retreiver.get_relevant_documents(input)

    # Create system and human message prompts
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template)

    # Create the chat prompt using the system and human message prompts
    conversation = [system_message_prompt, human_message_prompt]
    chat_prompt = ChatPromptTemplate.from_messages(conversation)
    response = gpt_4(chat_prompt.format_prompt(
        context=relevant_nodes,
        text=input).to_messages())

    return response.content

# Add argument parsing to allow for command-line input
parser = argparse.ArgumentParser(description='Generate HTML/CSS code based on input.')
parser.add_argument('input_text', type=str, help='The input text for generating code.')
args = parser.parse_args()

# Generate the code using the input argument
response = generate_code(args.input_text)

# Define the output file name
file_name = "output.html"

# Save the generated code to the output file
with open(file_name, "w") as file:
    file.write(response)
    print(f"HTML file saved as {file_name}")

# Open the HTML file in the default web browser
webbrowser_open_successful = webbrowser.open(file_name)
if webbrowser_open_successful:
    print("HTML file opened successfully in the default web browser.")
else:
    print("Failed to open the HTML file in the default web browser.")