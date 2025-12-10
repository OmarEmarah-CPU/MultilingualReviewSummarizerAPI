from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile, File, Form
from auth import register_client, verify_api_key
from preprocessing import preprocess_reviews
from language_utils import detect_and_translate_reviews
from summarizer import generate_summary
from keyword_semantics import semantic_keyword_detection
import pandas as pd
import io

app = FastAPI(title="Multilingual Review Summarizer API")


@app.post("/register")
async def register():
    api_key = register_client()
    return {"api_key": api_key}


@app.post("/process_reviews_excel")
async def process_reviews_excel(
    api_key: str = Depends(verify_api_key),
    file: UploadFile = File(...),
    keywords: str = Form(...)
):

    #Error Handling for different file types of datasets
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(await file.read()))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or Excel.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read file: {e}")


    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    
    # Detect review column (try best guess)
    text_column = None
    for col in df.columns:
        if "review" in col.lower():
            text_column = col
            break
    if text_column is None:
        # fallback to first column
        text_column = df.columns[0]

    reviews = df[text_column].dropna().astype(str).tolist()
    if not reviews:
        raise HTTPException(status_code=400, detail="No valid reviews found in the sheet.")


    clean_reviews = preprocess_reviews(reviews) #Calling the preprocessing file

    english_reviews = detect_and_translate_reviews(clean_reviews) #Detecting the language from language_utils.py


    summary = generate_summary(english_reviews) #Function called from summarizer file

    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
    keyword_results = semantic_keyword_detection(english_reviews, keyword_list)

    return {
        "summary": summary,
        "keyword_mapping": keyword_results,
        "total_reviews_processed": len(english_reviews)
    }