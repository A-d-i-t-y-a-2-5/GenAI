from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    
    host: Annotated[str, Field(default="0.0.0.0")]
    port: Annotated[int, Field(default=8000)]
    
if __name__ == "__main__":
    settings = AppSettings()
    print(settings)