import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in .env")
client = genai.Client(api_key=api_key)
MODEL = "gemini-3.1-flash-lite"

system_prompt = """
You are a job posting analyzer for a small recruitment analysis system.

You will receive a job posting and a list of the candidate's skills.
Analyze the job posting and extract the following information:
- title: The job title.
- required_experience_years: The minimum years of experience required.
- required_skills: A list of required skills.
- nice_to_have_skills: A list of nice-to-have skills.
- work_type: The type of work (e.g., remote, on-site, hybrid).
- salary_min: The minimum salary offered.
- salary_max: The maximum salary offered.
- salary_currency: The currency of the salary (e.g., USD, EUR, GEL).
- english_level: The required English proficiency level.
- skills_match: The candidate's skills that appear in the required skills.
- missing_skills: The required skills that the candidate does not have.

If a piece of information is not explicitly stated in the job posting,
return null for that field (or an empty list for list fields).
Do not guess or infer values that are not in the text.
"""

candidate_skills = "Python, FastAPI, PostgreSQL, Docker, Git"

job_postings = [
    # 1. Example from the instructions: all information is present
    """
    We are looking for a Python Backend Developer.
    The candidate should have at least 2 years of experience with
    Python and Django. Experience with PostgreSQL and Docker is required.
    The position is remote and the salary is $1500-$2500 per month.
    English B2 or higher is required.
    """,
    # 2. Different stack, hybrid work, salary in EUR, has nice-to-have skills
    """
    Our company is hiring a Data Engineer to join our team in Berlin.
    You need 3+ years of experience building data pipelines with Python and SQL.
    Hands-on experience with Apache Spark and Airflow is a must.
    Knowledge of Kafka and AWS is a plus.
    This is a hybrid role (3 days in the office).
    Salary: 4000-5500 EUR per month. Fluent English (C1) is required.
    """,
    # 3. Missing information: no experience, work type, salary, English level or nice-to-haves
    """
    Junior Frontend Developer wanted!
    Join our growing startup and help us build modern web applications.
    Required skills: JavaScript, React, HTML, CSS and Git.
    """,
]


class JobPosting(BaseModel):
    title: str
    required_experience_years: int | None
    required_skills: list[str]
    nice_to_have_skills: list[str]
    work_type: str | None
    salary_min: float | None
    salary_max: float | None
    salary_currency: str | None
    english_level: str | None
    skills_match: list[str] = Field(
        description="Candidate skills that appear in the required skills"
    )
    missing_skills: list[str] = Field(
        description="Required skills that the candidate does not have"
    )


for i, job_posting in enumerate(job_postings, start=1):
    contents = f"Job posting:\n{job_posting}\n\nCandidate skills:\n{candidate_skills}"

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=JobPosting,
        )
    )

    result = response.parsed

    print(f"===== Job posting #{i} =====")
    if result is None:
        print("Could not parse the response:")
        print(response.text)
    else:
        print(result.model_dump_json(indent=2))
    print()
