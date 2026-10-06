import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_PATH = PROJECT_ROOT / "mcp-server" / "server.py"


async def verify_server_protocol() -> None:
    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=str(PROJECT_ROOT),
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialized = await session.initialize()
            assert initialized.serverInfo.name == "kinuflow-project-context"

            tools = await session.list_tools()
            assert [tool.name for tool in tools.tools] == ["get_project_context"]

            expected_text = {
                "spec": "KinuFlow Specification",
                "api_contract": "openapi: 3.1.0",
                "instructions": "KinuFlow project instructions",
            }
            for section, expected in expected_text.items():
                result = await session.call_tool(
                    "get_project_context", {"section": section}
                )
                assert not result.isError
                assert expected in result.content[0].text

            invalid = await session.call_tool(
                "get_project_context", {"section": "arbitrary/path"}
            )
            assert invalid.isError


def test_server_initializes_and_exposes_only_fixed_read_tool() -> None:
    asyncio.run(verify_server_protocol())