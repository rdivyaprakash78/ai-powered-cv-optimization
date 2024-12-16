import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts import prompts
from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException
from typing import List
from langgraph.graph import START,END

load_dotenv()

class nodes :

    # Global variables definition
    def __init__(self):
        self.llm = ChatGroq(model = "llama-3.3-70b-versatile", temperature=0.25)
        self.api_key = os.getenv("GROQ_API_KEY")

    def keywords_extracting_agent(self, state):

        # Pydantic BaseModel definition for response
        class keywords_extracting_response(BaseModel):
            non_technical_keywords : List[str] = Field(description="List of extracted ATS friendly keywords that are missing in the CV based on the Job description")
            technical_keywords : List[str] = Field(description="List of extracted ATS friendly technical keywords that are missing in the CV based on the Job description")

        parser = PydanticOutputParser(pydantic_object= keywords_extracting_response)

        # Prompt for extracting keywords
        keywords_extractor_prompt = ChatPromptTemplate.from_messages([
            ("system", prompts["keywords extractor system prompt"]),
            ("human", prompts["keywords extractor human prompt"])
        ]
        )

        # Chain for extracting keywords
        keywords_extractor_chain = keywords_extractor_prompt | self.llm

        # Invoke the chain
        response = keywords_extractor_chain.invoke({
            "cv" : state["cv"],
            "job_description" : state["job_description"],
            "format_instructions" : parser.get_format_instructions()
        })

        # Parsing and recalling of llm if not parsed right
        try :
            parser.parse(response.content)
            evaluater_result = parser.parse(response.content)
        except OutputParserException as e:
            new_parser = OutputFixingParser.from_llm(parser=parser, llm=self.llm)
            evaluater_result = new_parser.parse(response.content)

        return {
            "technical_keywords" : evaluater_result.technical_keywords,
            "non_technical_keywords" : evaluater_result.non_technical_keywords
        }

