from langchain_community.utilities import SQLDatabase
from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, MessagesState, StateGraph

from agent.sql.tools import *
from app.settings import AppSettings

config = AppSettings()


model = ChatOpenRouter(
    model_name=f"{config.llm.provider}/{config.llm.model}",
    api_key=config.llm.api_key,
    temperature=config.llm.temperature,
)


db = SQLDatabase.from_uri("sqlite:///pokemon.db")

tools = get_tools(db, model)

configure_toolkit(model, tools, db)

builder = StateGraph(MessagesState)
builder.add_node(list_tables_v2)

builder.add_edge(START, "list_tables_v2")
agent = builder.compile()

agent.get_graph().draw_mermaid_png(output_file_path="graph.png")

question = "Which pokemon are the strongest?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
