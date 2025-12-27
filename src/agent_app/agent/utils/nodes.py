from prompts import *
from state import State, RoleClassification, StructuredResponse
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

load_dotenv(".env")


chat_model_name = os.environ.get("CHAT_MODEL_NAME")

def router(state: State) -> State:
    """
    Routes the query to the appropriate role based on the classification.
    """
    query = state['query']
    llm = ChatGroq(model=chat_model_name, temperature=0)
    llm_with_structured_output = llm.with_structured_output(RoleClassification)
    llm_with_structured_output.invoke(query)
    prompt = ROUTER_PROMPT.format(**state)
    # Simulate LLM call
    response = llm_call(prompt)
    # Parse response into QueryClassificationStructure
    classification: QueryClassificationStructure = parse_classification(response)
    return classification