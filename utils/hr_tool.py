import yaml


def prompt_selection(conv: str):
    """based on the input in the conversations select the appropriate prompt and return the prompt name"""
    with open("/workspaces/mcp_tools/src/prompts.yaml", "r") as f:
        data = yaml.safe_load(f)
    prompt_name = ""

    return prompt_name
