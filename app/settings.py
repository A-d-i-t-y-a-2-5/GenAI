from typing import Annotated, Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="OPENROUTER_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    provider: str = "openai"
    model: str = "gpt-4o-mini"
    api_key: str = "my-api-key"
    temperature: Annotated[float, Field(default=0.0, ge=0.0, le=1.0)]
    max_tokens: Annotated[Optional[int], Field(default=None, ge=1)]
    timeout: Annotated[Optional[int], Field(default=None, description="Timeout in milliseconds for API calls")]
    max_retries: Annotated[int, Field(default=2, ge=0)]
    
class ExtractorConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="EXTRACTOR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    user_name: Annotated[str, Field(default="user", description="Username for authentication")]
    password: Annotated[str, Field(default="password", description="Password for authentication")]
    keywords: Annotated[str, Field(default="", description="Keywords to search for in LinkedIn content")]
    sort_by: Literal["relevance", "date_posted"] = Field(default="relevance", description="Sorting criteria for LinkedIn search results")
    date_posted: Literal["past-24h", "past-week", "past-month"] = Field(default="past-24h", description="Filter for LinkedIn search results based on posting date")
    
    separator: Annotated[str, Field(default="Feed post", description="Exact phrase to split the LinkedIn page content into chunks")]
    chunk_size: Annotated[int, Field(default=8192, description="Maximum size of each chunk after splitting the LinkedIn page content")]
    
    scroll_duration: Annotated[int, Field(default=15, description="Duration in seconds to scroll the LinkedIn page to load content")]


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    host: Annotated[str, Field(default="0.0.0.0")]
    port: Annotated[int, Field(default=8000)]
    
    os_username: Annotated[str, Field(default="user", description="Windows username")]

    llm: LLMConfig = LLMConfig()
    extractor: ExtractorConfig = ExtractorConfig()


if __name__ == "__main__":
    settings = AppSettings()
    print(settings)