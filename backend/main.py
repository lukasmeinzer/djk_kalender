from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.build_ics.ics_creation import create_ics

app = FastAPI()

app.mount("/static", StaticFiles(directory="djk-kalender-app/src"), name="static")


@app.get("/download-ics/{team}")
async def download_ics(team: str):
    create_ics(team) # creates the file with newest data
    ics_file_path = Path(f"djk-kalender-app/src/spieltermine/{team}_alle_spiele.ics")
    
    if ics_file_path.exists():
        return FileResponse(
            ics_file_path,
            media_type='text/calendar',
            filename=ics_file_path.name,
            headers={"Content-Disposition": "attachment; filename=" + ics_file_path.name}  # Ensure attachment
        )
    else:
        return {"error": "Kontaktiere Lukas Meinzer"}


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("djk-kalender-app/src/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)