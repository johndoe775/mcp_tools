import asyncio
from fastmcp import Client

# Path to your server script (should be 'mcp_prompts.py' for stdio transport)
SERVER_PATH = "mcp_prompts.py"

# Input data for the prompt call
dummy_resume = """
## John Doe

**Software Engineer**  
San Francisco, CA  
john.doe@email.com | (555) 123-4567

### Experience
- Software Engineer, Acme Corp (2020–2025)
  - Built and maintained scalable web APIs in Python and Django
  - Led migration of legacy systems to cloud infrastructure (AWS)
  - Mentored junior engineers, conducted code reviews
### Projects
- Inventory Management System
  - Designed and implemented end-to-end inventory solution for retail client; stack: Flask, PostgreSQL
- Open Source Contributor: PyData Utils
  - Added new data import/export features and improved documentation
### Skills
- Languages: Python, JavaScript, SQL, C++
- Frameworks: Django, Flask, React
- Cloud: AWS, Docker, CI/CD
- Tools: Git, Linux, JIRA
### Education
B.Sc. Computer Science  
University of California, Berkeley  
2015–2019
"""

dummy_job_description = """
Seeking a Backend Developer skilled in Python, Django, and cloud technologies.
Responsibilities include API development, infrastructure migration, and mentoring team members.
Experience in PostgreSQL and CI/CD preferred.
"""

async def main():
    # Connect to the MCP server via stdio
    async with Client(SERVER_PATH) as client:
        # List available prompt tools (optional)
        prompts = await client.list_prompts()
        print("Available prompt tools:", [p.name for p in prompts])
        
        

        # Call your desired prompt (e.g., resume_and_job_decription_rewrite)
        """  result = await client.call_
            "resume_and_job_decription_rewrite",
            {
                "resume": dummy_resume,
                "job_description": dummy_job_description
            }
        )
        print("Result:\n", result.content[0].text)"""

if __name__ == "__main__":
    asyncio.run(main())
