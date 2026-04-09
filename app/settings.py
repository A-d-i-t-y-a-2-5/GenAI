from typing import Annotated, Optional
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

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    
    host: Annotated[str, Field(default="0.0.0.0")]
    port: Annotated[int, Field(default=8000)]
    
    llm: LLMConfig = LLMConfig()
    
if __name__ == "__main__":
    settings = AppSettings()
    print(settings)