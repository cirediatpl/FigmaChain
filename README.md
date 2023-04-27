# FigmaChain: HTML/CSS Code Generation from Figma Designs

FigmaChain is a set of Python scripts that generate HTML/CSS code based on Figma designs. Using OpenAI's GPT-3 model, FigmaChain enables developers to quickly generate HTML/CSS code from a Figma design input. It also includes a Streamlit-based chatbot interface for interactive code generation.

## Prerequisites

- Python 3.6 or higher
- An OpenAI API key (set as environment variable `OPENAI_API_KEY`)
- Access token, node IDs, and file key for Figma (set as environment variables `ACCESS_TOKEN`, `NODE_IDS`, and `FILE_KEY`)

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages: pip install openai langchain streamlit dotenv
4. Create a `.env` file in the project directory and add the following environment variables: OPENAI_API_KEY, ACCESS_TOKEN, NODE_IDS, FILE_KEY

## Usage

### generateCode.py

This script generates HTML/CSS code based on a user-provided input and a Figma design.

1. Navigate to the project directory.
2. Run the script with the desired input text as a command-line argument: python generateCode.py input_text
3. The script generates HTML/CSS code and saves it to an `output.html` file.
4. The script opens the generated HTML file in the default web browser.

### chatbot.py

This script provides a Streamlit-based chatbot interface for interactive code generation based on Figma designs.

1. Navigate to the project directory.
2. Start the Streamlit app: streamlit run chatbot.py
3. Open a web browser and go to the URL displayed in the terminal (e.g., `http://localhost:8501`).
4. Enter your input in the chat interface and receive generated HTML/CSS code.
5. The generated code is rendered on the page and the conversation is displayed.

## License

[MIT License](LICENSE)


