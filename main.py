from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models
from schemas import CandidateCreate, Candidate, Education, WorkingExperience, Family
from database import engine
from typing import List
from fastapi_pagination import  add_pagination, paginate
from fastapi_pagination.links import Page

models.Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_candidate(db: Session, candidate: CandidateCreate):
    db_candidate = models.Candidate(
        name=candidate.name,
        surname=candidate.surname,
        email=candidate.email,
        position=candidate.position,
        expect_salary=candidate.expect_salary,
        address=candidate.address,
        tel=candidate.tel,
        mobile=candidate.mobile,
        residence=candidate.residence,
        birthdate=candidate.birthdate,
        race=candidate.race,
        nationality=candidate.nationality,
        religion=candidate.religion,
        identity_card_no=candidate.identity_card_no,
        expiration_date=candidate.expiration_date,
        height=candidate.height,
        weight=candidate.weight,
        military_status=candidate.military_status,
        marital_status=candidate.marital_status,
        sex=candidate.sex,
        father_name=candidate.father_name,
        father_age=candidate.father_age,
        father_occupation=candidate.father_occupation,
        mother_name=candidate.mother_name,
        mother_age=candidate.mother_age,
        mother_occupation=candidate.mother_occupation,
        wife_husband_name=candidate.wife_husband_name,
        wife_husband_working_place=candidate.wife_husband_working_place,
        wife_husband_position=candidate.wife_husband_position,
        number_children=candidate.number_children,
        number_members_family=candidate.number_members_family,
        number_members_family_male=candidate.number_members_family_male,
        number_members_family_female=candidate.number_members_family_female,
        number_is_child_family=candidate.number_is_child_family,
    )
    if candidate.educations:
        for education_data in candidate.educations:
            education = models.Education(**education_data.dict())
            db_candidate.educations.append(education)
    
    if candidate.experiences:
        for experience_data in candidate.experiences:
            experience = models.WorkingExperience(**experience_data.dict())
            db_candidate.experiences.append(experience)
    
    if candidate.families:
        for family_data in candidate.families:
            family = models.Family(**family_data.dict())
            db_candidate.families.append(family)
            
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate



def read_candidate(candidate_id: int, db: Session):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


def update_candidate(db: Session, candidate_id: int, updated_candidate: CandidateCreate):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate.name=updated_candidate.name
    candidate.surname=updated_candidate.surname
    candidate.email=updated_candidate.email
    candidate.position=updated_candidate.position
    candidate.expect_salary=updated_candidate.expect_salary
    candidate.address=updated_candidate.address
    candidate.tel=updated_candidate.tel
    candidate.mobile=updated_candidate.mobile
    candidate.residence=updated_candidate.residence
    candidate.birthdate=updated_candidate.birthdate
    candidate.race=updated_candidate.race
    candidate.nationality=updated_candidate.nationality
    candidate.religion=updated_candidate.religion
    candidate.identity_card_no=updated_candidate.identity_card_no
    candidate.expiration_date=updated_candidate.expiration_date
    candidate.height=updated_candidate.height
    candidate.weight=updated_candidate.weight
    candidate.military_status=updated_candidate.military_status
    candidate.marital_status=updated_candidate.marital_status
    candidate.sex=updated_candidate.sex
    candidate.father_name=updated_candidate.father_name
    candidate.father_age=updated_candidate.father_age
    candidate.father_occupation=updated_candidate.father_occupation
    candidate.mother_name=updated_candidate.mother_name
    candidate.mother_age=updated_candidate.mother_age
    candidate.mother_occupation=updated_candidate.mother_occupation
    candidate.wife_husband_name=updated_candidate.wife_husband_name
    candidate.wife_husband_working_place=updated_candidate.wife_husband_working_place
    candidate.wife_husband_position=updated_candidate.wife_husband_position
    candidate.number_children=updated_candidate.number_children
    candidate.number_members_family=updated_candidate.number_members_family
    candidate.number_members_family_male=updated_candidate.number_members_family_male
    candidate.number_members_family_female=updated_candidate.number_members_family_female
    candidate.number_is_child_family=updated_candidate.number_is_child_family
    
    if not updated_candidate.educations and candidate.educations:
        for education_item in candidate.educations:
            delete_education(db, education_item.id)
    elif candidate.educations:
        intersect_educations = [item for item in candidate.educations if item.id not in [data_item.id for data_item in updated_candidate.educations]]
        if intersect_educations:
            for intersect_item in intersect_educations:
                delete_education(db, intersect_item.id)
        
    if updated_candidate.educations:
        for education_data in updated_candidate.educations:
            if not education_data.id:
                education = models.Education(**education_data.dict())
                candidate.educations.append(education)
            else:
                education_item = db.query(models.Education).filter(models.Education.id == education_data.id).first()
                if education_item:
                    education_item.institution = education_data.institution
                    education_item.education_level = education_data.education_level
                    education_item.institution = education_data.institution
                    education_item.major = education_data.major
                    education_item.from_year = education_data.from_year
                    education_item.to_year = education_data.to_year
    
    if not updated_candidate.experiences and candidate.experiences:
        for education_item in candidate.experiences:
            delete_experience(db, education_item.id)
    elif candidate.experiences:
        intersect_working_experiences = [item for item in candidate.experiences if item.id not in [data_item.id for data_item in updated_candidate.experiences]]
        if intersect_working_experiences:
            for intersect_item in intersect_working_experiences:
                delete_experience(db, intersect_item.id)
        
    if updated_candidate.experiences:
        for experience_data in updated_candidate.experiences:
            if not experience_data.id:
                education = models.WorkingExperience(**experience_data.dict())
                candidate.experiences.append(education)
            else:
                experience_item = db.query(models.WorkingExperience).filter(models.WorkingExperience.id == experience_data.id).first()
                if experience_item:
                    experience_item.company = experience_data.company
                    experience_item.position = experience_data.position
                    experience_item.job_description = experience_data.job_description
                    experience_item.salary = experience_data.salary
                    experience_item.reasons_resignation = experience_data.reasons_resignation
                    experience_item.from_year = experience_data.from_year
                    experience_item.to_year = experience_data.to_year
                    
    if not updated_candidate.families and candidate.families:
        for family_item in candidate.families:
            delete_family(db, family_item.id)
    elif candidate.families:
        intersect_families = [item for item in candidate.families if item.id not in [data_item.id for data_item in updated_candidate.families]]
        if intersect_families:
            for intersect_item in intersect_families:
                delete_family(db, intersect_item.id)
        
    if updated_candidate.families:
        for family_data in updated_candidate.families:
            if not family_data.id:
                family = models.Family(**family_data.dict())
                candidate.families.append(family)
            else:
                family_item = db.query(models.Family).filter(models.Family.id == family_data.id).first()
                if family_item:
                    family_item.name = family_data.name
                    family_item.age = family_data.age
                    family_item.occupation = family_data.occupation

    db.commit()
    db.refresh(candidate)
    return candidate


def delete_education(db: Session, _id: int):
    education = db.query(models.Education).filter(models.Education.id == _id).first()
    if education is None:
        raise HTTPException(status_code=404, detail="Education not found")
    db.delete(education)
    db.commit()


def delete_experience(db: Session, _id: int):
    workingExperience = db.query(models.WorkingExperience).filter(models.WorkingExperience.id == _id).first()
    if workingExperience is None:
        raise HTTPException(status_code=404, detail="WorkingExperience not found")
    db.delete(workingExperience)
    db.commit()


def delete_family(db: Session, _id: int):
    family = db.query(models.Family).filter(models.Family.id == _id).first()
    if family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    db.delete(family)
    db.commit()

    
def delete_candidate(db: Session, candidate_id: int):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(candidate)
    db.commit()


@app.post("/candidates/")
def create_candidate_api(candidate: CandidateCreate, db: Session = Depends(get_db)):
    return create_candidate(db, candidate)


@app.get("/candidates/{candidate_id}", response_model=Candidate)
def read_candidate_api(candidate_id: int, db: Session = Depends(get_db)):
    return read_candidate(candidate_id, db)


@app.put("/candidates/{candidate_id}")
def update_candidate_api(candidate_id: int, updated_candidate: Candidate, db: Session = Depends(get_db)):
    return update_candidate(db, candidate_id, updated_candidate)


@app.delete("/candidates/{candidate_id}")
def delete_candidate_api(candidate_id: int, db: Session = Depends(get_db)):
    delete_candidate(db, candidate_id)
    return {"message": "Candidate deleted successfully"}


@app.get("/candidates/", response_model=Page[Candidate])
def read_candidates(page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).offset(page).limit(limit).all()
    return paginate(candidates) 

add_pagination(app)