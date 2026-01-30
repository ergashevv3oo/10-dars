from pydantic import BaseModel
from typing import Optional


class DoctorCreate(BaseModel):
    full_name: str
    age: int
    phone_number: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    name: str
    age: int
    doctor_id: int


class PatientResponse(PatientCreate):
    id: int
    image: Optional[str] = None
    video: Optional[str] = None

    class Config:
        from_attributes = True
