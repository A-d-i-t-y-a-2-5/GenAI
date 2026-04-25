from langchain_community.utilities import SQLDatabase
from langchain_openrouter import ChatOpenRouter
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

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

get_schema_tool =tools["sql_db_schema"]
get_schema_node = ToolNode([get_schema_tool], name="get_schema")

run_query_tool = tools["sql_db_query"]
run_query_node = ToolNode([run_query_tool], name="run_query")

configure_toolkit(model, tools, db)

builder = StateGraph(MessagesState)
builder.add_node(list_tables_v2)
builder.add_node(call_get_schema)
builder.add_node(get_schema_node, "get_schema")
builder.add_node(generate_query)
builder.add_node(check_query_v2)
builder.add_node(call_run_query)
builder.add_node(run_query_node, "run_query")

builder.add_edge(START, "list_tables_v2")
builder.add_edge("list_tables_v2", "call_get_schema")
builder.add_edge("call_get_schema", "get_schema")
builder.add_edge("get_schema", "generate_query")
builder.add_conditional_edges(
    "generate_query",
    should_continue,
)
builder.add_edge("check_query_v2", "call_run_query")
builder.add_edge("call_run_query", "run_query")
builder.add_edge("run_query", "generate_query")

agent = builder.compile()

agent.get_graph().draw_mermaid_png(output_file_path="graph.png")

question = "Which pokemon are the strongest under total of 600?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
