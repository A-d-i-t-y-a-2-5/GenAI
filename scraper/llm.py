from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openrouter import ChatOpenRouter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from scraper.schema import JobPostingList


class LanguageModel:
    def __init__(self, config: BaseSettings):
        self.config = config

        model = ChatOpenRouter(
            model_name=f"{config.llm.provider}/{config.llm.model}",
            api_key=config.llm.api_key,
            temperature=config.llm.temperature,
            max_tokens=config.llm.max_tokens,
            timeout=config.llm.timeout,
            max_retries=config.llm.max_retries,
        )

        self.structured_model = model.with_structured_output(JobPostingList)

        self.splitter = RecursiveCharacterTextSplitter(
            separators=[config.extractor.separator],  # exact phrase to split on
            chunk_size=config.extractor.chunk_size,
            chunk_overlap=0,
            is_separator_regex=False,
        )

        self.system_message = SystemMessage(
            content="Extract structured data from the job posting  present in the webpage content below. Use null or empty string for missing fields depending on the schema."
        )
        
    def split_document(self, doc: Document) -> list[Document]:
        chunks = self.splitter.split_documents([doc])
        print(f"Total chunks created: {len(chunks)}")
        return chunks
    
    def generate_inputs(self, chunks: list[Document]) -> list[list[SystemMessage | HumanMessage]]:
        return [
            [
                self.system_message,
                HumanMessage(content=chunk.page_content),
            ]
            for chunk in chunks
        ]
        
    def merge_results(self, results: list[JobPostingList]) -> JobPostingList:
        all_jobs = []
        for result in results:
            all_jobs.extend(result.jobs)
        
        return JobPostingList(jobs=all_jobs)
    
    def generate_response(self, inputs: list[list[SystemMessage | HumanMessage]]) -> JobPostingList:
        results = self.structured_model.batch(inputs, config={"max_concurrency": 5})
        return self.merge_results(results)
    
    