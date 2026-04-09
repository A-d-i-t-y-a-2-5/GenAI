from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_sync_playwright_browser,  # Use sync version
)

# At module level - this works
sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()

tools_by_name = {tool.name: tool for tool in tools}
navigate_tool = tools_by_name["navigate_browser"]
get_elements_tool = tools_by_name["get_elements"]

print("Navigating to CNN World...")
navigate_tool.run(
    {"url": "https://web.archive.org/web/20230428133211/https://cnn.com/world"},
    verbose=True,
    run_name="Navigate to CNN World",
)

get_elements_tool.run(
    {"selector": ".container__headline", "attributes": ["innerText"]}, verbose=True, run_name="Get CNN World Headlines"
)


