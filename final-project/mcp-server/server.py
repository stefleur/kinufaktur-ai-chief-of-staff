from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTEXT_FILES = {
    "spec": "product-spec.md",
    "api_contract": "openapi.yaml",
    "instructions": "AGENTS.md",
}

mcp = FastMCP("kinuflow-project-context")


@mcp.tool()
def get_project_context(
    section: Literal["spec", "api_contract", "instructions"],
) -> str:
    """Read one fixed KinuFlow project context file by its allowed section."""
    return (PROJECT_ROOT / CONTEXT_FILES[section]).read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")