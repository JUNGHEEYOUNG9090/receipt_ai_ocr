from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL(
    pipeline_version="v1.6"
)

output = pipeline.predict(
    input="images/receipt_test_03.jpg"
)

for res in output:
    res.print()