from paddleocr import PaddleOCRVL


pipeline = PaddleOCRVL(
    pipeline_version="v1.6"
)


def run_ocr(file_path):
    output = pipeline.predict(
        input=file_path
    )

    results = list(output)

    ocr_text = []

    for res in results:
        data = res.json

        for item in data.get("res", {}).get("parsing_res_list", []):
            content = item.get("block_content")

            if content:
                ocr_text.append(content)

    return "\n".join(ocr_text)