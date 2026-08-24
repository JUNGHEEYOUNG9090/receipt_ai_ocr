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

중요한 규칙:
1. items는 반드시 배열([])로 반환하세요. 상품이 없거나 확인하기 어려운 경우에도 null을 사용하지 말고 빈 배열 []을 사용하세요.
2. 상품 항목이 하나라도 OCR 결과에서 추정 가능하면 반드시 items에 포함하세요.
3. 상품명, 단가, 수량, 금액 중 확인할 수 없는 개별 값은 null로 처리하세요.
4. OCR 오류가 명확한 경우 문맥에 맞게 보정하세요.
5. supply_amount, vat, total_amount는 계산식을 사용하지 말고 최종 숫자값만 입력하세요.
6. JSON 객체는 정확히 하나만 반환하세요.
7. 마크다운 코드 블록(```json ... ```)을 사용하지 마세요.
8. 설명, 계산 과정, 수정 과정, 추가 문장을 출력하지 마세요.

반드시 다음 형식의 JSON 객체 하나만 반환하세요.

{{
  "merchant_name": "...",
  "transaction_date": "...",
  "items": [
    {{
      "name": "...",
      "unit_price": 0,
      "quantity": 1,
      "amount": 0
    }}
  ],
  "supply_amount": 0,
  "vat": 0,
  "total_amount": 0
}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text