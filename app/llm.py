import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_receipt_data(ocr_text, system_prompt):

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_prompt,
        input=ocr_text
    )

    return response.output_text