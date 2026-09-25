from typing import Annotated

from fastapi import FastAPI, UploadFile, File

from app.ocr import run_ocr

import shutil
import os
import time


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ocr")
async def ocr(
    files: Annotated[list[UploadFile], File()]
):
    total_start = time.perf_counter()

    print("\n========== OCR START ==========")

    os.makedirs("uploads", exist_ok=True)

    results = []

    for file in files:
        print(f"\n파일 처리 시작 : {file.filename}")

        file_path = os.path.join(
            "uploads",
            file.filename
        )

        upload_start = time.perf_counter()

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        upload_time = time.perf_counter() - upload_start

        print(f"1. 파일 저장 완료 : {upload_time:.3f}초")
        print(f"   파일 : {file.filename}")

        # OCR
        print("2. OCR 추론 시작")

        ocr_start = time.perf_counter()

        ocr_text = run_ocr(file_path)

        ocr_time = time.perf_counter() - ocr_start

        print(f"3. OCR 추론 완료 : {ocr_time:.3f}초")

        print("\n[OCR 결과]")
        print(ocr_text)

        results.append({
            "filename": file.filename,
            "upload_time": round(upload_time, 3),
            "ocr_time": round(ocr_time, 3),
            "ocr_text": ocr_text
        })

    total_time = time.perf_counter() - total_start

    print(f"\n4. 전체 처리 완료 : {total_time:.3f}초")
    print("=========== OCR END ===========\n")

    return {
        "status": "success",
        "files": results,
        "total_time": round(total_time, 3)
    }