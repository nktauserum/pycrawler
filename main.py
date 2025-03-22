import trafilatura
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UrlInput(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Welcome to Web Scraping API"}

@app.post("/extract")
async def extract_content(url_input: UrlInput):
    try:
        downloaded = trafilatura.fetch_url(url_input.url)
        result = trafilatura.extract(downloaded, include_formatting=False, include_links=False, include_images=False, include_tables=False, only_with_metadata=True, output_format='json')
        if result:
            result_dict = json.loads(result)
            return {
                "title":    result_dict["title"],
                "sitename": result_dict["source-hostname"],
                "text":     result_dict["raw_text"]
            }

        else:
            return {"error": "No content extracted"}
        
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
