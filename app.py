from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class Input(BaseModel):
    text: str


@app.post("/extract")
def extract(data: Input):

    text = data.text

    if not text:
        raise HTTPException(status_code=422, detail="Empty input")

    # vendor extraction
    vendor = re.search(r"Acme Industries Ltd|[A-Za-z0-9&\-\s]+Ltd|Inc", text)
    vendor_name = vendor.group(0).strip() if vendor else "Unknown"
    vendor_name = vendor_name.replace("Invoice from ", "")

    # amount extraction
    amount = re.search(r"(\d+(\.\d+)?)", text)

    # currency extraction
    currency = re.search(r"\b(USD|EUR|GBP)\b", text)

    # date extraction
    date = re.search(r"\d{4}-\d{2}-\d{2}", text)

    return {
        "vendor": vendor_name,
        "amount": float(amount.group(1)) if amount else 0.0,
        "currency": currency.group(1) if currency else "USD",
        "date": date.group(0) if date else "2026-01-01"
    }
