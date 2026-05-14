from io import StringIO
from typing import Literal

from langchain.messages import AIMessage
from langchain.tools import BaseTool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import tool
from langgraph.graph import END, MessagesState
import matplotlib.pyplot as plt
import pandas as pd
from pydantic import BaseModel, Field

from agent.sql.prompts import (
    generate_query_system_prompt,
    check_query_system_prompt,
)

model: BaseLanguageModel | None = None
tools: dict[str, BaseTool] | None = None
db: SQLDatabase | None = None

class PlotResultInput(BaseModel):
    """Recommendation of appropriate data visualizations based on the user's question, SQL query, and query results"""
    data_table: str = Field(description="The data table (results of an SQL query) for which to recommend visualizations, formatted as a CSV string.")
    plot_type: Literal["bar", "line", "pie", "scatter"] | None = Field(default=None, description="The type of graph to plot")
    x: str = Field(description="Column to use from data for x axis")
    y: list[str] = Field(description="Column(s) to use from data for y axis")

@tool(args_schema=PlotResultInput)
def plot(data_table: str, plot_type: str, x: str, y: list[str]) -> str:
    """Generate a plot from a pandas DataFrame and save it as an image."""
    try:
        df = pd.read_csv(StringIO(data_table))
        if plot_type == "line":
            df.plot(x=x, y=y, kind="line")
        elif plot_type == "bar":
            df.plot(x=x, y=y, kind="bar")
        plt.savefig("plot.png")
        return "Plot saved as plot.png"
    except Exception as e:
        return f"Error generating plot: {str(e)}"



def get_tools(db: SQLDatabase, llm: BaseLanguageModel):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    tools.append(plot)
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
            top_k=20,
        ),
    }
    # We do not force a tool call here, to allow the model to
    # respond naturally when it obtains the solution.
    llm_with_tools = model.bind_tools([tools["sql_db_query"]])
    response = llm_with_tools.invoke([system_message] + state["messages"])

    return {"messages": [response]}

def suggest_visualization(state: MessagesState):
    llm_with_tools = model.bind_tools([tools["plot"]], tool_choice="any")
    response = llm_with_tools.invoke([state["messages"][-1]])
    return {"messages": [response]}

def check_query_v2(state: MessagesState):
    tool_calls = state["messages"][-1].tool_calls
    query_checker_tool = tools["sql_db_query_checker"]
    tool_messages = [query_checker_tool.invoke(tool_call) for tool_call in tool_calls]

    return {"messages": tool_messages}


def call_run_query(state: MessagesState):
    llm_with_tools = model.bind_tools([tools["sql_db_query"]], tool_choice="any")
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}

def run_query_v2(state: MessagesState):
    query_tool = tools["sql_db_query"]
    
    content = state["messages"][-1].content
    if content.startswith("```sql\n") and content.endswith("\n```"):
        query = content[len("```sql\n") : -len("\n```")]
    else:
        query = content
    query = query.strip()
    
    # Content format: ```sql\n<query>;\n```
    tool_call = {
        "name": "sql_db_query",
        "args": {"query": query},
        "id": state["messages"][-1].id,
        "type": "tool_call",
    }
    
    ai_message = AIMessage(content="", tool_calls=[tool_call])

    tool_message = query_tool.invoke(tool_call)

    return {"messages": [ai_message, tool_message]}


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
        return "suggest_visualization"
    else:
        return "check_query_v2"
