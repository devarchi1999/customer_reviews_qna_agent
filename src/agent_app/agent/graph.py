from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Literal
from utils.nodes import get_inputs_from_query,router, run_regional_manager, run_store_manager, run_executive_manager
from utils.state import State, StructuredResponse
from utils.tools import RetrievalWithFilter, EmbeddingGenerator


graph = StateGraph(State)
graph.add_node("get_inputs_from_query", get_inputs_from_query)
graph.add_node("executive_manager_node", run_executive_manager)
graph.add_node("store_manager_node", run_store_manager)
graph.add_node("regional_manager_node", run_regional_manager)

graph.add_edge(START, "get_inputs_from_query")
graph.add_conditional_edges("get_inputs_from_query", 
                            router,{"Executive Manager":"executive_manager_node",
                                    "Store Manager":"store_manager_node",
                                    "Regional Manager":"regional_manager_node",
                                    })

graph.add_edge("executive_manager_node", END)
graph.add_edge("store_manager_node", END)
graph.add_edge("regional_manager_node", END)
app = graph.compile()
# app.get_graph(xray=True).draw_png("agent_graph.png")

result = app.invoke({"query": '''I am the executive manager and I have noticed a decline in customer satisfaction in the region4 and store5.\n
                     Can you provide insights into the main issues customers are facing in this region and suggest actionable steps to improve their experience?''',
                     })
