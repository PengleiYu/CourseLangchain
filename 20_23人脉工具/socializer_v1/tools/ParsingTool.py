from langchain.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field


class TextParsing(BaseModel):
    summary: str = Field(description='大V个人简介')
