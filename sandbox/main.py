import modal
from deepagents import create_deep_agent
from langchain_openrouter import ChatOpenRouter
from langchain_modal import ModalSandbox
from pydantic import BaseModel

from app.settings import AppSettings

config = AppSettings()

model = ChatOpenRouter(
    model_name=f"{config.llm.provider}/{config.llm.model}",
    api_key=config.llm.api_key,
    temperature=config.llm.temperature,
)

app = modal.App.lookup("test", create_if_missing=True)
modal_sandbox = modal.Sandbox.create(app=app)
backend = ModalSandbox(sandbox=modal_sandbox)


class Row(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str


class Rows(BaseModel):
    rows: list[Row]


with open("sandbox/mock_data.csv", "rb") as f:
    backend.upload_files(
        [
            ("/mock_data.csv", f.read()),
        ]
    )

agent = create_deep_agent(
    model=model,
    system_prompt="You are a Python coding assistant with sandbox access. You are to write a Python script to answer the user's request and return the answer.",
    backend=backend,
    response_format=Rows,
)


try:
    for chunk in agent.stream(
        {
            "messages": [
                {
                    "role": "system",
                    "content": "You are to write a Python script to answer the user's request and return the answer.",
                },
                {
                    "role": "user",
                    "content": "Write a Python script to return the first 5 female users from the CSV file.",
                }
            ]
        },
        stream_mode="values",
    ):
        chunk["messages"][-1].pretty_print()
finally:
    modal_sandbox.terminate()
