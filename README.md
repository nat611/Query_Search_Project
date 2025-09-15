# Query_Search_Project
This project takes user queries and calls on an LLM to return the query as a JSON parsed structured.

## Setup Instructions

- To run, make sure Python (3.8+) is installed, then install the Hugging Face Hub client via `pip install huggingface_hub` through your terminal.

- The `InferenceClient()` from `huggingface_hub` requires authentication, so a Hugging Face account must be made. After creating an account, go to https://huggingface.co/settings/tokens and generate a new token with read access. Copy and save the unique token key (this will always begin as hf_...)

- After cloning the github repository, the script can be run by opening the terminal, navigating to the correct dictionary containing the Python script, and run the script using the command: `python file_name.py`. But before running make sure to change "hf_token" in line 60 (`hf_token = os.environ.get("hf_token")`) with your unique token key! 

- Using the CLI you will be prompted to enter a query- type your query and press enter. The script will then call the LLM and output the parsed JSON directly in the terminal. 
