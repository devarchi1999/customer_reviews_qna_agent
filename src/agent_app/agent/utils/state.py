from typing_extensions import Literal, TypedDict


class State(TypedDict):
    query: str
    role: Literal['Executive', 'Store Manager', 'Regional Manager']
    sentiment: Literal['positive', 'negative']
    region: str
    store: str
    
class RoleClassification(TypedDict):
    role: Literal['Executive', 'Store Manager', 'Regional Manager']
    sentiment: Literal['positive', 'negative']
    region: list[str]
    store: list[str]
    
class StructuredResponse(TypedDict):
    role: str
    answer: str
    supporting_facts: list[str]