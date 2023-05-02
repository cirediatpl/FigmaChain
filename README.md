# FigmaChain: HTML/CSS Code Generation from Figma Designs

FigmaChain is a set of Python scripts that generate HTML/CSS code based on Figma designs. Using OpenAI's GPT-3 model, FigmaChain enables developers to quickly generate HTML/CSS code from a Figma design input. It also includes a Streamlit-based chatbot interface for interactive code generation.

## Prerequisites

- Python 3.6 or higher
- An OpenAI API key (set as environment variable `OPENAI_API_KEY`)
- Access token, node IDs, and file key for Figma (set as environment variables `ACCESS_TOKEN`, `NODE_IDS`, and `FILE_KEY`)

## Accessing the Figma RESTful API

To access the Figma RESTful API, you will need an access token, node IDs, and a file key.

- **File Key**: The file key can be pulled from the URL of the Figma design file. For example, the file key in the URL `https://www.figma.com/file/{filekey}/sampleFilename` is `{filekey}`.
- **Node IDs**: Node IDs are also available in the URL. Click on any element in the Figma design file and look for the `?node-id={node_id}` parameter in the URL.
- **Access Token**: Instructions for obtaining an access token can be found in the Figma help center article: https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens


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

This is the chatbot code. 

1. Start the Streamlit app: streamlit run chatbot.py
2. Enter your input in the chat interface and receive generated HTML/CSS code.
3. The generated code is rendered on the page and the conversation is displayed.

## Sponsors

✨ Learn to build projects like this one (with an early bird discount): [BuildFast Course](https://www.buildfastcourse.com/)

## License

[MIT License](LICENSE)



