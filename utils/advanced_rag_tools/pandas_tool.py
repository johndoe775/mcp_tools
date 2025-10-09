import os
import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.tools import tool
from .state import GraphState
from .helpers import LLM


@tool
def pandas_tool(state: GraphState):
    """
    use this tool when the user asks for visualiztion from the data using pandas
    """

    def capture_df_info(df: pd.DataFrame) -> str:
        """
        Capture the output of df.info() into a string.
        """
        buffer = io.StringIO()
        df.info(buf=buffer)
        return buffer.getvalue()

    def load_dataframes(csv_dir: str):
        """
        Reads all CSV files in csv_dir, returns:
        - paths: dict mapping dataframe name to its file path
        - df_infos: dict mapping dataframe name to its .info() string
        - globals_dict: dict to be used as globals when executing code
        Also registers each DataFrame in globals_dict under its name.
        """
        paths = {}
        df_infos = {}
        globals_dict = {}

        for fname in os.listdir(csv_dir):
            if fname.lower().endswith(".csv"):
                name = os.path.splitext(fname)[0]
                path = os.path.join(csv_dir, fname)

                # Read once, store in dicts
                df = pd.read_csv(path)
                paths[name] = path
                df_infos[name] = capture_df_info(df)
                globals_dict[name] = df.copy()

        return paths, df_infos, globals_dict

    def generate_visualization_code(df_infos: dict, purpose: str) -> str:
        """
        Given a mapping of dataframe names to their info-strings and an analysis purpose,
        returns only the seaborn/matplotlib code needed for the visualization.
        """
        prompt_template = """
    You are a data analysis expert. The user has these dataframes (with info shown) 
    and wants to achieve a given analysis purpose.

    ### Instructions:
    *** use name from df_info dictionary to create a dataframe using paths["name"] to access the path
    1) Do NOT tamper with original dataframes; use df.copy() if needed.
    2) Always reference df.info() to confirm column names and dtypes.
    3) Do NOT hallucinate column names: only use those present.
    4) Recommend the single best chart or minimal set of charts.
    5) If merging is needed, do it within the sns call.
    6) Do all data calculations on separate lines before plotting.
    7) Output ONLY the Python code lines (no comments, no narrative ,no preamble) and not even language of the code must be mentioned.

    ### DataFrames Info:
    {df_infos}

    ### Purpose of Analysis:
    {purpose}


    ### Example output code:

    import pandas
    import numpy

    df.info()
    """
        template = PromptTemplate(
            input_variables=["df_infos", "purpose"], template=prompt_template
        )
        # Assuming you have an LLM instance named `llm` defined elsewhere
        chain = template | LLM().llm
        code = chain.invoke({"df_infos": df_infos, "purpose": purpose})
        return code.content.strip()

        # if you need to load environment variables for LLM API keys

    # 1) Load CSV files from a directory
    csv_dir = "/data"  # update this path if needed
    paths, df_infos, global_vars = load_dataframes(csv_dir)

    # 2) Show the first few rows for user sanity check (optional)
    for name, df in global_vars.items():
        print(f"--- {name}.head() ---")
        print(df.head(), "\n")

    # 3) Get analysis purpose from user input
    purpose = input("Enter the purpose of analysis: ").strip()
    if not purpose:
        print("No purpose entered. Exiting.")
        return

    # 4) Generate visualization code from the LLM
    code = generate_visualization_code(df_infos, purpose)
    print("\n===== Generated Visualization Code =====\n")
    cleaned_code = code.replace("`", "").replace("python", "")
    print(cleaned_code)
    exec_namespace = {**global_vars, "paths": paths}
    # 5) Execute and display plots
    print("\n===== Executing Code =====\n")
    for line in cleaned_code.splitlines():
        try:
            # Preprocessing or new column creation
            if not line.lstrip().startswith(("sns.", "plt.")):
                exec(line, exec_namespace)
            else:
                plt.figure(figsize=(10, 6))
                exec(line, exec_namespace)
                plt.show()
        except Exception as e:
            print(f"Error executing `{line}`: {e}")
    state["message"].append("completed pandas visualization")
    return state
