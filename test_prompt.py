import yaml
import asyncio
from fastmcp import Client, FastMCP

mcp = FastMCP(name="YAMLPrompts")


def make_prompt_function(name, template, description, inputs):
    param_names = list(inputs.keys())
    param_str = ", ".join(param_names)
    # Compose the function code string
    code = f"def {name}({param_str}):\n"
    code += f"    '''{description}'''\n"
    fmt_params = ", ".join([f"{k}={k}" for k in param_names])
    code += f"    return f'''{template}'''.format({fmt_params})\n"
    # Compile function into a namespace
    namespace = {}
    exec(code, {}, namespace)
    return namespace[name]


# Load YAML
with open(r"C:\Users\jorda\Downloads\my_stuff\projects\mcp_tools\mcp_tools\src\prompts.yaml") as f:
    yaml_data = yaml.safe_load(f)

for prompt_key, info in yaml_data.items():
    prompt_template = info["prompt"]
    description = info.get("tool_use_case", "")
    inputs = info["inputs"]  # This is already {"resume": "resume", ...}
    fn = make_prompt_function(prompt_key, prompt_template, description, inputs)
    mcp.prompt(fn)


if __name__ == "__main__":
    # run over HTTP on port 8000 to match your examples
    mcp.run(transport="stdio")
