import io
import os
import pandas as pd
import numpy
from .helpers import LLM
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from .state import GraphState


# pysqldf = lambda q: sqldf(q, globals())


@tool
def pandasql_tool(state: GraphState):
    """
    use this tool when the user asks for data analysis using SQL (via pandasql)
    """
    from pandasql import sqldf

    pysqldf = lambda q: sqldf(q, globals())

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
        - globals_dict: dict to be used as globals when executing queries
        Also registers each DataFrame in globals_dict under its name.
        """
        paths = {}
        df_infos = {}
        globals_dict = {}

        for fname in os.listdir(csv_dir):
            if fname.lower().endswith(".csv"):
                name = os.path.splitext(fname)[0]
                path = os.path.join(csv_dir, fname)

                df = pd.read_csv(path)
                paths[name] = path
                df_infos[name] = capture_df_info(df)
                globals_dict[name] = df.copy()

        return paths, df_infos, globals_dict

    def generate_sql_code(df_infos: dict, question: str) -> str:
        """
        Given a mapping of dataframe names to their info-strings and a user question,
        returns only the SQL query (no narrative, no comments).
        """
        prompt_template = """
You are an expert in SQL-based data analysis. The user has these tables (with schema & info shown)
and wants to answer a specific question using SQL. Use pandasql / SQLite dialect.

### Instructions:
1) Only reference tables by the names given in the df_infos keys.
2) Only use columns shown in the DataFrame info—do not invent any.
3) If you need to JOIN tables, do so explicitly.
4) Output ONLY a single SQL query that directly answers the question. No explanation, no comments.
5) Do not wrap the query in backticks or quotes.

### Tables Info:
{df_infos}

### Question:
{question}
"""
        template = PromptTemplate(
            input_variables=["df_infos", "question"], template=prompt_template
        )
        chain = LLMChain(llm=LLM().llm, prompt=template)
        response = chain.run({"df_infos": df_infos, "question": question})
        return response.strip()

    # 1) Load CSV files
    csv_dir = "/content"  # adjust if needed
    paths, df_infos, global_vars = load_dataframes(csv_dir)

    # 2) Optionally, show schemas for sanity check
    for name, info in df_infos.items():
        print(f"--- Schema for {name} ---")
        print(info, "\n")

    # 3) Get the analysis question from the user
    question = state["inputs"].strip()
    if not question:
        print("No question entered. Exiting.")
        return state

    # 4) Ask the LLM to generate a pandasql query
    sql_query = generate_sql_code(df_infos, question)
    print("\n===== Generated SQL Query =====\n")
    print(sql_query, "\n")

    # 5) Execute the SQL via pandasql
    print("===== Executing SQL Query =====")
    pysqldf = lambda q: sqldf(q, global_vars)
    try:
        result_df = pysqldf(sql_query)
        print(result_df)
    except Exception as e:
        print(f"Error executing query: {e}")

    # 6) Update state if needed
    state["messages"].append("completed pandasql analysis")
    return state
