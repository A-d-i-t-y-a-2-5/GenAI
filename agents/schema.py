from typing import Optional

from pydantic import BaseModel, Field

class JobPosting(BaseModel):
    poster: str = Field(description="Name of the person who posted the job")
    company: Optional[str] = Field(description="Company name")
    role: str = Field(description="Job title")
    location: Optional[str] = Field(
        description="Job location E.g., 'Bengaluru' or 'Remote'"
    )
    experience: Optional[str] = Field(description="Experience level if mentioned")
    salary: Optional[str] = Field(description="Salary range if mentioned")


class JobPostingList(BaseModel):
    """Container for multiple job postings extracted from a page."""

    jobs: list[JobPosting]