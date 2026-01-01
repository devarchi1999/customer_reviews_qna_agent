from typing_extensions import Literal, TypedDict, Any


class State(TypedDict):
    query: str
    role: Literal['Executive', 'Store Manager', 'Regional Manager']
    sentiment: Literal['positive', 'negative']
    region: str
    store: str
    retrieval_tool: Any
    embedding_generator: Any
    
class RoleClassification(TypedDict):
    role: Literal['Executive Manager', 'Store Manager', 'Regional Manager']
    sentiment: Literal['positive', 'negative','none']
    region: list[str]
    store: list[str]
    
class StructuredResponse(TypedDict):
    role: str
    region: str
    store: str
    sentiment: str
    answer: str
    supporting_facts: list[str]