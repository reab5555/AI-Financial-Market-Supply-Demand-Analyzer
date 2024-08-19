import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# Load environment variables
load_dotenv()

# OpenAI API configuration
#openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = 'your_openai_api_key'

# LLM model configuration
MODEL = "gpt-4o-mini"

# Initialize ChatOpenAI
chat = ChatOpenAI(model_name=MODEL, temperature=0.1, openai_api_key=openai_api_key)


class ProductCategory(BaseModel):
    category: str = Field(description="The product category or type")
    suppliers: List[str] = Field(description="List of stock symbols for companies supplying this product category")


class ProductCategoryList(BaseModel):
    categories: List[ProductCategory] = Field(description="List of product categories and their suppliers")


# Output parser
output_parser = PydanticOutputParser(pydantic_object=ProductCategoryList)


def get_product_prompt(initial_date, n_categories, market_index):
    template = """As an analyst in finance, list {n_categories} types or categories of products that were in high demand as of {initial_date}.
    Also mention which companies provide these products or services - stocks must be from the {market_index} index.

    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(template)

    return prompt.format_messages(
        initial_date=initial_date,
        n_categories=n_categories,
        market_index=market_index,
        format_instructions=output_parser.get_format_instructions()
    )


def get_product_data(initial_date, n_categories, market_index):
    messages = get_product_prompt(initial_date, n_categories, market_index)
    response = chat(messages)
    return output_parser.parse(response.content)