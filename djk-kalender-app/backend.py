from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="src"), name="static")

@app.get("/get-ics-files/{folder}")
async def get_ics_files(folder: str):
    directory_path = f"src/{folder}"
    try:
        files = [f for f in os.listdir(directory_path) if f.endswith('.ics')]
        return JSONResponse(content=files)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)