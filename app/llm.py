import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_receipt_data(ocr_text):

    prompt = f"""
다음은 영수증 OCR 결과입니다.

OCR 결과:
{ocr_text}

OCR 결과를 분석하여 영수증 정보를 JSON으로 정리하세요.

다음 정보를 추출하세요.

- merchant_name: 가맹점명
- transaction_date: 거래일시
- items: 상품 목록
  - name: 상품명
  - unit_price: 단가
  - quantity: 수량
  - amount: 금액
- supply_amount: 공급가액
- vat: 부가세
- total_amount: 합계금액

OCR 오류가 명확한 경우 문맥에 맞게 보정하세요.
확실하지 않은 값은 null로 처리하세요.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text