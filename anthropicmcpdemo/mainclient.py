from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="uv",
    args=["run", "main.py"],
    env=None,
)

# Optional: create a sampling callback
async def handle_sampling_message(
    context,
    params: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello world from model!",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # Initialize the connection
            await session.initialize()
            tools = await session.list_tools()
            print("################################# TOOLS #####################################")
            print("Tools:", tools)
            print("################################ RESOURCES #####################################")
            resources = await session.list_resources()
            print("Resources:", resources)
            print("################################# PROMPTS #####################################")
            prompts = await session.list_prompts()
            print("Prompts:", prompts)

            #invocando a herramientas
            print("############################ TOOL TESTING - ADD #####################################")
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            if result.content and len(result.content) > 0:
                content = result.content
                print("Add numbers result:", str(content))

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())