from utils.prompts import router_prompt, regional_manager_prompt, store_manager_prompt, executive_manager_prompt
from utils.state import State, RoleClassification, StructuredResponse
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
from utils.tools import RetrievalWithFilter, EmbeddingGenerator
from typing_extensions import Literal

load_dotenv(".env")
chat_model_name = os.environ.get("CHAT_MODEL_NAME") 
llm = ChatGroq(model=chat_model_name,temperature=0,max_tokens=None,reasoning_format="parsed",timeout=None,
               max_retries=2)   
    
def get_inputs_from_query(state: State) -> State:
    """
    Routes the query to the appropriate role based on the classification.
    """
    query = state['query']

    llm_for_role_classification = llm.with_structured_output(RoleClassification)
    
    prompt = [("system", router_prompt),("human", query),]
    response = llm_for_role_classification.invoke(prompt)

    
    return {'role': response['role'],
            'region': response['region'],
            'store': response['store'],
            'sentiment': response['sentiment'],
            'embedding_generator': EmbeddingGenerator(),
            'retrieval_tool': RetrievalWithFilter()
            }

def router(state: State) -> Literal['Executive Manager', 'Store Manager', 'Regional Manager']:
    return state['role']

    
    
def run_regional_manager(state: State) -> StructuredResponse:
    """
    Executes the Regional Manager role to answer the query using RAG approach.
    """
    query = state['query']
    role = state['role']
    region = state['region']
    store = state['store']
    sentiment = state['sentiment']
    retrieval_tool = state['retrieval_tool']
    embedding_generator = state['embedding_generator']
    
    # Create filter for retrieval based on region and store
    filter_criteria = {}
    if region:
        filter_criteria['region'] = {'$in': region}
    if store:
        filter_criteria['store'] = {'$in': store}
    if sentiment and sentiment != 'none':
        filter_criteria['sentiment'] = sentiment
    else:
        filter_criteria['sentiment'] = {'$in': ['positive', 'negative']}
    
    # Retrieve relevant documents
    retrieval_response = retrieval_tool.retrieve(query=query, top_k=10, filter=filter_criteria)
    documents = [item['metadata']['review_text'] for item in retrieval_response['matches']]
    
    # Prepare context for LLM
    context = "\n\n".join(documents)

    llm_for_regional_manager = llm.with_structured_output(StructuredResponse)
    
    #alternative store value for llm response
    if store == []:
        store = "all_stores"
    
    prompt_template = f'''User Query: {query}\n\n
                          Context: {context}\n\n
                          role: {role}\n\n
                          region: {region}\n\n
                          store: {store}\n\n
                          sentiment: {sentiment}'''
    
    prompt = [("system", regional_manager_prompt),
              ("human", prompt_template),]
    response = llm_for_regional_manager.invoke(prompt) 

    print(prompt_template)
    print(response)

    return response
    
    
def run_store_manager(state: State) -> StructuredResponse:
    """
    Executes the Store Manager role to answer the query using RAG approach.
    """
    query = state['query']
    role = state['role']
    region = state['region']
    store = state['store']
    sentiment = state['sentiment']
    retrieval_tool = state['retrieval_tool']
    embedding_generator = state['embedding_generator']

    
    # Create filter for retrieval based on region and store
    filter_criteria = {}
    if region:
        filter_criteria['region'] = {'$in': region}
    if store:
        filter_criteria['store'] = {'$in': store}
    if sentiment and sentiment != 'none':
        filter_criteria['sentiment'] = sentiment
    else:
        filter_criteria['sentiment'] = {'$in': ['positive', 'negative']}
    
    # Retrieve relevant documents
    retrieval_response = retrieval_tool.retrieve(query=query, top_k=10, filter=filter_criteria)
    documents = [item['metadata']['review_text'] for item in retrieval_response['matches']]
    
    # Prepare context for LLM
    context = "\n\n".join(documents)
    
    llm_for_store_manager = llm.with_structured_output(StructuredResponse)
    
    #alternative region value for llm response
    if region == []:
        region = "no_region_specified"
    
    prompt_template = f'''User Query: {query}\n\n
                          Context: {context}\n\n
                          role: {role}\n\n
                          region: {region}\n\n
                          store: {store}\n\n
                          sentiment: {sentiment}'''
    
    prompt = [("system", store_manager_prompt),
              ("human", prompt_template),]
    
    response = llm_for_store_manager.invoke(prompt)

    print(prompt_template)
    print(response)
    
    return response


def run_executive_manager(state: State) -> StructuredResponse:
    """
    Executes the Executive role to answer the query using RAG approach.
    """
    query = state['query']
    region = state['region']
    store = state['store']
    sentiment = state['sentiment']
    role = state['role']
    retrieval_tool = state['retrieval_tool']

    
    # Create filter for retrieval based on region and store
    filter_criteria = {}
    if region:
        filter_criteria['region'] = {'$in': region}
    if store:
        filter_criteria['store'] = {'$in': store}
    if sentiment and sentiment != 'none':
        filter_criteria['sentiment'] = sentiment
    else:
        filter_criteria['sentiment'] = {'$in': ['positive', 'negative']}
    
    # Retrieve relevant documents
    retrieval_response = retrieval_tool.retrieve(query=query, top_k=10, filter=filter_criteria)
    documents = [item['metadata']['review_text'] for item in retrieval_response['matches']]
    
    # Prepare context for LLM
    context = "\n\n".join(documents)
    
    llm_for_executive_manager = llm.with_structured_output(StructuredResponse)
    
    #alternative store & region value for llm response
    if store == []:
        store = "all_stores"
    if region == []:
        region = "all_regions"
    
    prompt_template = f'''User Query: {query}\n\n
                          Context: {context}\n\n
                          role: {role}\n\n
                          region: {region}\n\n
                          store: {store}\n\n
                          sentiment: {sentiment}'''
    
    
    prompt = [("system", regional_manager_prompt),
              ("human", prompt_template),]
    
    response = llm_for_executive_manager.invoke(prompt)

    print(prompt_template)
    print(response)
    
    return response