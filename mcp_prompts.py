from fastmcp import FastMCP

mcp = FastMCP(name="JobAutomationServer")

@mcp.prompt
def resume_and_job_decription_rewrite(resume: str, job_description: str) -> str:
    """
    Rewrite the following resume to match the job description provided:
    
    Resume: {resume}
    
    Job Description: {job_description}
    
    Instructions:
    1) Use the available experience, projects, and skills to rewrite the resume.
    2) Don't Halucinate.
    3) Don't use any external data but only the resume and job description.
    4) Don't mention any comments or notes and preamble in the response.
    5) Give the output in markdown format with proper orientation and formatting.
    """
    return f"""
Rewrite the following resume to match the job description provided:
    
Resume: {resume}
    
Job Description: {job_description}
    
Instructions:
1) Use the available experience, projects, and skills to rewrite the resume.
2) Don't Halucinate.
3) Don't use any external data but only the resume and job description.
4) Don't mention any comments or notes and preamble in the response.
5) Give the output in markdown format with proper orientation and formatting.
"""

@mcp.prompt
def cold_mail_and_person_info(resume: str, personal_info: str) -> str:
    """
    Using the following resume, write a professional and inquisitive cold mail tailored to a personal information of the recruiter, seeking job opportunities.
    Make sure that the entire message is conveyed in not more than 5 lines:
    Resume: {resume}
    Person Information of the recruiter: {personal_info}
    Instructions:
    1) Start with the salutation "Hi."
    2) Write in the first person.
    3) Utilize only the experience, projects, and skills from the resume to craft the email; do not include any external data or assumptions.
    4) Maintain a professional and inquisitive tone, expressing interest in job opportunities.
    5) Do not include any comments or preamble in the response.
    7) Conclude with "Regards," followed by the name of the person whose resume is being used.
    8) Format the output in markdown as an email with proper orientation and paragraphing.
    """
    return f"""
Using the following resume, write a professional and inquisitive cold mail tailored to the personal information of the recruiter, seeking job opportunities
Make sure that the entire message is conveyed in not more than 5 lines:

Resume: {resume}

Person Information of the recruiter: {personal_info}

Instructions:
1) Start with the salutation "Hi."
2) Write in the first person.
3) Utilize only the experience, projects, and skills from the resume to craft the email; do not include any external data or assumptions.
4) Maintain a professional and inquisitive tone, expressing interest in job opportunities.
5) Do not include any comments or preamble in the response.
7) Conclude with "Regards," followed by the name of the person whose resume is being used.
8) Format the output in markdown as an email with proper orientation and paragraphing.
"""

@mcp.prompt
def cold_mail_no_personal_info(resume: str) -> str:
    """
    Using the following resume, write a generic professional and inquisitive cold mail seeking job opportunities ,Make sure that the entire message is conveyed in not more than 5 lines. No personal information about the recipient is provided.
    Resume: {resume}
    Instructions:
    -1) Start with salutaion hi
    0) write in first person.
    1) Use the available experience, projects, and skills from the resume to write the cold mail.
    2) The tone must be professional and inquisitive, seeking job opportunities.
    3) Don't hallucinate.
    4) Don't use any external data but only the resume.
    5) Don't mention any comments and preamble in the response.
    7) End with regards and the name of ther person whose resume is being used.
    8) Give the output in markdown format in email format with proper orientation and use regards as ending greeeting followed by the name of the person from the resume
    9)Make sure that mail is properly paragraphed and formatted.
    """
    return f"""
Using the following resume, write a generic professional and inquisitive cold mail seeking job opportunities ,Make sure that the entire message is conveyed in not more than 5 lines. No personal information about the recipient is provided.

Resume: {resume}

Instructions:
-1) Start with salutaion hi
0) write in first person.
1) Use the available experience, projects, and skills from the resume to write the cold mail.
2) The tone must be professional and inquisitive, seeking job opportunities.
3) Don't hallucinate.
4) Don't use any external data but only the resume.
5) Don't mention any comments and preamble in the response.
7) End with regards and the name of ther person whose resume is being used.
8) Give the output in markdown format in email format with proper orientation and use regards as ending greeeting followed by the name of the person from the resume
9)Make sure that mail is properly paragraphed and formatted.
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")
