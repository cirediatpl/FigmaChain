import os
import re
import openai
import streamlit as st
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import streamlit.components.v1 as components
from streamlit_chat import message
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()

# Set the OpenAI API key and dataset path from the environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Define the file name of the HTML file to read and the updated file name
file_name = "output.html"
updated_file_name = "output_updated.html"

st.title('FigmaChain')

# Define the chatbot template
template = """Assistant is a senior developer. Assistant only writes new code and does not write additional text.
Assistant is designed to assist with front-end development incorporating modern design principles such as responsive design.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of code, and can use this knowledge to provide accurate and informative coding updates.
Overall, Assistant is a powerful tool that can help with a wide range of design and development tasks.
{history}
Human: {human_input}
Assistant:"""

# Define the chatbot prompt
prompt = PromptTemplate(
    input_variables=["history", "human_input"], 
    template=template
)

# Initialize the LLMChain for the chatbot
chatgpt_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, request_timeout=120), 
    prompt=prompt, 
    verbose=True, 
    memory=ConversationBufferWindowMemory(k=2),
)

# Function to read the HTML content from the specified file
def read_html_content(file_name):
    with open(file_name, "r") as file:
        html_content = file.read()
    return html_content

# Function to write the HTML content to the specified file
def write_html_content(html_content):
    with open(updated_file_name, "w") as file:
        file.write(html_content)

# Function to check if the output is a valid HTML/CSS code update
def is_valid_html_css_code(output):
    pattern = re.compile(r'<.*?>|{.*?}')
    return bool(pattern.search(output))

# Function to generate a response using OpenAI's ChatCompletion API
def generate_response(prompt, html_content):
    completion = chatgpt_chain.predict(
        human_input=(
            "You are a senior developer. I want you to improve the following code with the following {prompt}: {html_content}. Only output new html/css code. Do not write additional text."
            "The code is html/css that was created by AI based on a Figma document."
        ).format(prompt=prompt, html_content=html_content)
    )
    return completion

# Function to render the HTML content using Streamlit's markdown function
def render_html(html_content):
    components.html(html_content, scrolling=True, height=300)

# Function to get the user's input from the text input field
def get_text():
    # Create a Streamlit input field and return the user's input
    input_text = st.text_input("", key="input")
    return input_text

# Initialize the session state for generated responses and past inputs
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['I am ready to help you update your Figma design']

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hello']

# Initialize current_html_content with the content of the original HTML file
if 'current_html_content' not in st.session_state:
    st.session_state['current_html_content'] = read_html_content(file_name)

# Render the initial HTML content
display = render_html(read_html_content(file_name))

# Get the user's input from the text input field
user_input = get_text()

# If there is user input, search for a response and update the HTML content
if user_input:
    html_content = read_html_content(file_name)
    output = generate_response(user_input, st.session_state['current_html_content'])
    if is_valid_html_css_code(output):
        # Update the chatbot with the new design 
        st.session_state['current_html_content'] = output
        # Write the updated HTML content to the file
        write_html_content(output)

        # Append the user input and generated output to the session state
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

        # Render the updated HTML content
        render_html(output)

# If there are generated responses, display the conversation using Streamlit messages
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))


