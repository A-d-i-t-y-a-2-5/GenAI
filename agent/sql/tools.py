from typing import Literal

from langchain.messages import AIMessage
from langchain.tools import BaseTool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.language_models import BaseLanguageModel
from langgraph.graph import END, MessagesState

from agent.sql.prompts import (
    generate_query_system_prompt,
    check_query_system_prompt,
)

model: BaseLanguageModel | None = None
tools: dict[str, BaseTool] | None = None
db: SQLDatabase | None = None


def get_tools(db: SQLDatabase, llm: BaseLanguageModel):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    return {tool.name: tool for tool in tools}


def configure_toolkit(
    llm: BaseLanguageModel, tool_collection: dict[str, BaseTool], database: SQLDatabase
):
    global model, tools, db
    model = llm
    tools = tool_collection
    db = database


def list_tables_v2(state: MessagesState):
    tool_call = {
        "name": "sql_db_list_tables",
        "args": {},
        "id": "abc123",
        "type": "tool_call",
    }
    tool_call_message = AIMessage(content="", tool_calls=[tool_call])

    list_tables_tool = tools["sql_db_list_tables"]
    tool_message = list_tables_tool.invoke(tool_call)
    response = AIMessage(f"Available tables: {tool_message.content}")

    return {"messages": response}


def call_get_schema(state: MessagesState):
    llm_with_tools = model.bind_tools([tools["sql_db_schema"]], tool_choice="any")
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def generate_query(state: MessagesState):
    system_message = {
        "role": "system",
        "content": generate_query_system_prompt.format(
            dialect=db.dialect,
            top_k=5,
        ),
    }
    # We do not force a tool call here, to allow the model to
    # respond naturally when it obtains the solution.
    llm_with_tools = model.bind_tools([tools["sql_db_query"]])
    response = llm_with_tools.invoke([system_message] + state["messages"])

    return {"messages": [response]}


def check_query_v2(state: MessagesState):
    tool_call = state["messages"][-1].tool_calls[0]
    query_checker_tool = tools["sql_db_query_checker"]
    tool_message = query_checker_tool.invoke(tool_call)

    return {"messages": [tool_message]}


def call_run_query(state: MessagesState):
    llm_with_tools = model.bind_tools([tools["sql_db_query"]], tool_choice="any")
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def check_query(state: MessagesState):
    system_message = {
        "role": "system",
        "content": check_query_system_prompt.format(dialect=db.dialect),
    }

    # Generate an artificial user message to check
    tool_call = state["messages"][-1].tool_calls[0]
    user_message = {"role": "user", "content": tool_call["args"]["query"]}
    llm_with_tools = model.bind_tools([tools["sql_db_query"]], tool_choice="any")
    response = llm_with_tools.invoke([system_message, user_message])
    response.id = state["messages"][-1].id

    return {"messages": [response]}


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return END
    else:
        return "check_query_v2"
