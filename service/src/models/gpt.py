from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
import os
from IPython.display import display, Markdown

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


model = ChatOpenAI(model="gpt-4o", temperature=0, seed=1337)


class WorkGrading(BaseModel):
    grade_score: float = Field(
        description="analyze the homework and give a grade 2 (lowest) and 6 (highest) in (you can use 0.5 intervals)."
    )
    feedback: list = Field(
        description="create a key points list to explain why you grade the homework with this score"
    )


class WorkPlagiatism(BaseModel):
    probability: dict = Field(
        description="""Provide a dictionary with 2 keys 'human' and 'ai' each with probabity for AI generated content after
analyzing the word order, text structure, gramatical errors and other factors valuable for the classification.
Consider wrong style, inconsistency, errors more likely as a human writing"""
    )
    feedback: str = Field(
        description="create a feedback in markdown numerical list with example phrases to explain your opinion"
    )


parser = PydanticOutputParser(pydantic_object=WorkGrading)


def generate_chain(prompt: PromptTemplate, model, parser):
    return prompt | model | parser
