import os
from huggingface_hub import InferenceClient
import json

prompt = """

    You are an interface for a search engine that analyses user queries to extract user intent and relevant details. 
    Your task is to convert user queries into a parsed JSON structure that captures the user's intent, relevant categories, relevant filters, and a brief summary of the query. 
    The output should always contain the users intent and a summary. Other fields depend on the user intent. A wide range of user intents are possible, including but not limited to: product_search, navigation_search, informational_fact_recall, informational_explanation, instructional_search, transaction_search, recommendation_search, news_search, generative_request, problem_solving ...etc.
    If the user query does not fit any of the predefined intents, classify it as "general_search".
    If there is any sort of product, transaction, or recommendation related intent, make sure to include product categories, relevant filters, prices ranges, and other relevant details. 
    If the user query is vague or ambiguous, make your best guess based on the context and information provided. User queries can often be short and lack grammatical structure, so use your judgement to interpret the query meaning. 

        OUTPUT INSTRUCTIONS: 
    - Return only valid JSON
    - Do NOT add Markdown, code fences, or any explanation
    - The output must start with { and end with }

    IMPORTANT: If the user query is simply too vague, prompt the user for clarification and return the JSON structure: {"error": "Sorry, I didn't understand your question. Could you provide more detail? :)"}


    Example: 
    Input: "Good cafes in Edinburgh for matcha lattes under £10"
    Output:
    {"intent": "local_search", "category": "cafes", "location": "Edinburgh", "filters": {"drink": "matcha lattes", "price": "<£10"}, "summary": "User is looking for cafes in Edinburgh that serve matcha lattes and cost less than £10."}

    """

# initialize the client 
client = InferenceClient()

# parsing logic : want to make sure that the output is in json format
def parse_response(response):
    try:
        return json.loads(response)
    
    except json.JSONDecodeError:
        print("Error: Model returned invalid JSON. Raw output:")
        print(response)
        return {"error": "invalid_json", "raw_response": response}

# error class to handle unexpected errors
class Error(Exception):
    pass

# query analyser function (prompt logic)
def analyse_query(query: str): # takes user query as input, returns parsed structure
    if len(query.strip().split()) == 1:
        return {"error": "query_too_short", "message": "Please provide more detail."}

    try: 
        completion = client.chat.completions.create(
            # model="deepseek-ai/DeepSeek-V3-0324" ,
            model = "openai/gpt-oss-20b" , 
            messages=[
                {"role": "system", "content": prompt}, # system prompt 
                {"role": "user", "content": query} # user query
            ],

            max_tokens=500, # limit response length
        )

        output = completion.choices[0].message.content # get content of the response
        return parse_response(output)
    
    except Exception as e: # highlights the query that caused an error and displays the original error 
        raise Error(f"Failed to respond to query: {query} \nError: {e}")

# I/O logic: how the input is taken and how the output is displayed
if __name__ == "__main__":
    user_query = input("Enter your query: ")
    try: 
        result = analyse_query(user_query)
        print("-Analysis Result-")
        print(json.dumps(result, indent=2))  # nicely print json output
    except Error as e: # highlighting unexpected errors
        print("Oops! Something went wrong:", e)