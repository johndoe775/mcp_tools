from mcp.server.fastmcp.server import FastMCP
from mcp_tools import data, tool_maker


mcp = FastMCP("HR Server")


@mcp.tool()
def greet(name: str) -> str:
    """A simple tool that greets a person by name."""
    return f"Hello, {name}!"


@mcp.tool()
def resume_rewrite(resume, job_description, personal_info=""):
    """use this tool to rewrite resume making it more appealing to the job description"""
    response = tool_maker(resume, job_description, personal_info).llm_fx(
        list(data.keys())[0]
    )
    return response


@mcp.tool()
def cold_mail_info_present(
    resume,
    personal_info,
    job_description="",
):
    """use this tool to write a cold mail to a recruiter when you have personal info about them"""
    response = tool_maker(resume, job_description, personal_info).llm_fx(
        list(data.keys())[1]
    )
    return response


@mcp.tool()
def cold_mail_with_no_info(resume, job_description="", personal_info=""):
    """use this tool to write a cold mail to a recruiter when you have no personal info about them"""
    response = tool_maker(resume, job_description, personal_info).llm_fx(
        list(data.keys())[2]
    )
    return response


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
