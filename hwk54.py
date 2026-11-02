from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

MODEL_NAME = "gemini-3.5-flash-lite"

model = ChatGoogleGenerativeAI(
    model=MODEL_NAME
)

class ProductReview(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(..., description="The sentiment of the review.")
    pros: list[str] = Field(..., description="The positive aspects of the product.")
    cons: list[str] = Field(..., description="The negative aspects of the product.")
    summary: str = Field(..., description="A brief summary of the review.")
    recommend: bool = Field(..., description="Whether the model recommends the product (True or False).")

parser = PydanticOutputParser(pydantic_object=ProductReview)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
            You are a helpful assistant.
            Analyze the following product review and provide:
            1. The sentiment of the review: positive, negative, or neutral.
            2. The positive aspects of the product.
            3. The negative aspects of the product.
            4. A brief summary of the review.
            5. Whether you recommend the product (True or False).
            
            {format_instructions}
        """),
        ("human", "{review}")
    ]
)

chain = prompt | model | parser

reviews = [
    "This laptop is fast, lightweight, and has an excellent display. However, its battery life could be better.",
    "The phone is slow, overheats frequently, and the camera quality is disappointing.",
    "The headphones have average sound quality. They are comfortable, but the price is relatively high."
]

for review in reviews:
    response = chain.invoke(
        {
            "review": review,
            "format_instructions": parser.get_format_instructions()
        }
    )
    print("========================================")
    print(f"Review: {review}")
    print(f"Response: {response}")
    print(f"Response Type: {type(response)}")
    print("========================================")
