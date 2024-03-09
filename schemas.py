from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class FamilyBase(BaseModel):
    name: str
    age: str
    occupation: str


class FamilyCreate(FamilyBase):
    pass


class Family(FamilyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class EducationBase(BaseModel):
    education_level: str
    institution: str
    major: str
    from_year: str
    to_year: str


class EducationCreate(EducationBase):
    pass


class Education(EducationBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class WorkingExperienceBase(BaseModel):
    company: str
    from_year: str
    to_year: str
    position: str
    job_description: str
    salary: float
    reasons_resignation: str


class WorkingExperienceCreate(WorkingExperienceBase):
    pass


class WorkingExperience(WorkingExperienceBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class CandidateBase(BaseModel):
    name: str
    surname: str
    email: str
    position: Optional[str] = None
    expect_salary: Optional[float] = None
    address: Optional[str] = None
    tel: Optional[str] = None
    mobile: Optional[str] = None
    residence: Optional[str] = None
    birthdate: Optional[date] = None
    race: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    identity_card_no: Optional[str] = None
    expiration_date: Optional[date] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    military_status: Optional[str] = None
    marital_status: Optional[str] = None
    sex: Optional[str] = None
    father_name: Optional[str] = None
    father_age: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_age: Optional[str] = None
    mother_occupation: Optional[str] = None
    wife_husband_name: Optional[str] = None
    wife_husband_working_place: Optional[str] = None
    wife_husband_position: Optional[str] = None
    number_children: Optional[int] = None
    number_members_family: Optional[int] = None
    number_members_family_male: Optional[int] = None
    number_members_family_female: Optional[int] = None
    number_is_child_family: Optional[int] = None
    educations: Optional[List[EducationCreate]] = None
    experiences: Optional[List[WorkingExperienceCreate]] = None
    families: Optional[List[FamilyCreate]] = None


class CandidateCreate(CandidateBase):
    pass


class Candidate(CandidateBase):
    id: Optional[int] = None
    educations: Optional[List[Education]] = None
    experiences: Optional[List[WorkingExperience]] = None
    families: Optional[List[Family]] = None

    class Config:
        orm_mode = True
