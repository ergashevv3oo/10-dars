from sqlalchemy.ext.asyncio import AsyncSession
from models import Doctor, Patient
from schemas import DoctorCreate, DoctorResponse, PatientCreate, PatientResponse


async def create_doctor(doctor: DoctorCreate, db: AsyncSession) -> DoctorResponse:
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    return DoctorResponse.model_validate(db_doctor)


async def create_patient(
    patient: PatientCreate,
    image: str | None,
    video: str | None,
    db: AsyncSession
) -> PatientResponse:
    db_patient = Patient(
        name=patient.name,
        age=patient.age,
        doctor_id=patient.doctor_id,
        image=image,
        video=video
    )
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return PatientResponse.model_validate(db_patient)
