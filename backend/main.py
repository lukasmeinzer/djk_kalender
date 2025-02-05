from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from build_ics.ics_creation import create_ics


app = FastAPI()

app.mount("/static", StaticFiles(directory="djk-kalender-app/src"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("djk-kalender-app/src/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/get-ics-files/{team}")
async def get_ics_files(team: str):
    # Warte bis ics Dateien erstellt wurden
    create_ics(team)
    
    # Dann gucke hier nach den Dateien
    directory_path = f"djk-kalender-app/src/spieltermine_{team}"
    try:
        files = [f for f in os.listdir(directory_path) if f.endswith('.ics')]
        list_return = []
        for f in files:
            dict_temp = {}
            dict_temp["Datei"] = f
            timestamp = f.split(".ics")[0].split("_")[1]
            dt = datetime.strptime(timestamp, "%Y%m%dT%H%M%S")
            dict_temp["Datum"] = dt.date().isoformat()
            dict_temp["Gegner"] = f.split("_")[0]
            list_return.append(dict_temp)
        return JSONResponse(content=list_return)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)