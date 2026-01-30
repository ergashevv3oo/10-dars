from fastapi import FastAPI, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from database import engine, Base, get_db
from schemas import DoctorCreate, DoctorResponse, PatientResponse
from crud import create_doctor, create_patient

app = FastAPI()

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@app.post("/doctor", response_model=DoctorResponse)
async def add_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await create_doctor(doctor, db)


@app.post("/patient", response_model=PatientResponse)
async def add_patient(
    name: str = Form(...),
    age: int = Form(...),
    doctor_id: int = Form(...),
    image: UploadFile = None,
    video: UploadFile = None,
    db: AsyncSession = Depends(get_db)
):
    image_path = None
    video_path = None

    if image:
        image_path = f"{MEDIA_DIR}/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(await image.read())

    if video:
        video_path = f"{MEDIA_DIR}/{video.filename}"
        with open(video_path, "wb") as f:
            f.write(await video.read())

    patient_data = {
        "name": name,
        "age": age,
        "doctor_id": doctor_id
    }

    return await create_patient(
        patient=type("obj", (), patient_data),
        image=image_path,
        video=video_path,
        db=db
    )


if __name__ == "__main__":
    uvicorn.run(app)
