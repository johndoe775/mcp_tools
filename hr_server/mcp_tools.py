import yaml
from llm import LLM
from langchain.prompts import PromptTemplate


with open(r"C:\Users\jorda\Downloads\my_stuff\projects\mcp_tools\mcp_tools\src\prompts.yaml") as file:
    #yaml_data = yaml.safe_load(f)
    data = yaml.safe_load(file)


class tool_maker:
    def __init__(self, resume:str , job_description: str = None, personal_info: str = None):
        self.resume = resume
        self.job_description = job_description
        self.personal_info = personal_info
        self.data = data

    def llm_fx(self, key) -> str:
        f"""{self.data[key]["tool_use_case"]}"""
        input_variables = list(self.data[key]["inputs"].keys())
        template = self.data[key]["prompt"].format(
            resume=self.resume,
            job_description=self.job_description,
            personal_info=self.personal_info,
        )
        prompt_template = PromptTemplate(
            input_variables=input_variables, template=template
        )
        chain = prompt_template | LLM().llm
        response = chain.invoke(self.data[key]["inputs"]).content

        return response
