import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts import prompts
from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException

load_dotenv()

class nodes :

    # Global variables definition
    def __init__(self):
        self.llm = ChatGroq(model = "llama-3.3-70b-versatile", temperature= 0)
        self.api_key = os.getenv("GROQ_API_KEY")

    # Generater function
    def generater(self, state):
        
        # Pydantic BaseModel definition for response
        class generater_response(BaseModel):
            cv : str = Field(description="Generated CV")
        
        generater_response_parser = PydanticOutputParser(pydantic_object= generater_response)

        # Prompt for generating CV
        generater_prompt = ChatPromptTemplate.from_messages([
            ("system", prompts["generater system prompt"]),
            ("human", prompts["generater human message prompt"])
        ]
        )

        # Chain for generating CV
        generater_chain = generater_prompt | self.llm

        # Invoke the chain
        response = generater_chain.invoke({
        "base_cv" : state["cv"],
        "job_description" : state["job_description"],
        "keywords" : state["keywords"],
        "suggestions" : state["suggestions"],
        "format_instructions" : generater_response_parser.get_format_instructions()
        })

        # Parsing and recalling of llm if not parsed right
        try :
            generater_response_parser.parse(response.content)
            result = generater_response_parser.parse(response.content)
        except OutputParserException as e:
            new_parser = OutputFixingParser.from_llm(parser=generater_response_parser, llm=self.llm)
            result = new_parser.parse(response.content)

        # Updating state with generated CV
        return {"cv" : state["cv"]}
