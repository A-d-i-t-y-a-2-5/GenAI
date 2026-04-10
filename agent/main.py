# References:
# - https://github.com/langchain-ai/langchain/issues/15605

import asyncio
import typing

from langchain.agents import create_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_openrouter import ChatOpenRouter
from playwright.async_api import async_playwright, Browser

from app.settings import AppSettings


async def create_async_playwright_browser(
    headless: bool = True, args: typing.Optional[typing.List[str]] = None
) -> Browser:
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless, args=args)
    return browser


async def setup_agent():
    browser = await create_async_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    tools = toolkit.get_tools()

    agent_chain = create_agent(
        model=model,
        tools=tools,
    )
    return agent_chain, browser


async def main():
    agent, browser = await setup_agent()
    try:
        print("Asking agent to get headers from langchain.com...")
        result = await agent.ainvoke(
            {"messages": [("user", "What are the headers on langchain.com?")]}
        )
        print(result["messages"][-1].content)
    finally:
        await browser.close()


config = AppSettings()


model = ChatOpenRouter(
    model_name=f"{config.llm.provider}/{config.llm.model}",
    api_key=config.llm.api_key,
    temperature=config.llm.temperature,
)

if __name__ == "__main__":
    asyncio.run(main())
