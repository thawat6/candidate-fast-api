from sqlalchemy import  Column, Integer, String, ForeignKey, Float, Date, DateTime
from sqlalchemy.orm import  relationship
from database import Base
from sqlalchemy.sql import func

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    position = Column(String)
    expect_salary = Column(Float)
    address = Column(String)
    tel = Column(String)
    mobile = Column(String)
    residence = Column(String)
    birthdate = Column(Date)
    race = Column(String)
    nationality = Column(String)
    religion = Column(String)
    identity_card_no = Column(String)
    expiration_date = Column(Date)
    height = Column(String)
    weight = Column(String)
    military_status = Column(String)
    marital_status = Column(String)
    sex = Column(String)
    father_name = Column(String)
    father_age = Column(String)
    father_occupation = Column(String)
    mother_name = Column(String)
    mother_age = Column(String)
    mother_occupation = Column(String)
    wife_husband_name = Column(String)
    wife_husband_working_place = Column(String)
    wife_husband_position = Column(String)
    number_children = Column(Integer)
    number_members_family = Column(Integer)
    number_members_family_male = Column(Integer)
    number_members_family_female = Column(Integer)
    number_is_child_family = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    families = relationship('Family', back_populates='candidate')
    educations = relationship('Education', back_populates='candidate')
    experiences = relationship('WorkingExperience', back_populates='candidate')

class Family(Base):
    __tablename__ = "families"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(String)
    occupation = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    candidate = relationship('Candidate', back_populates='families')
    
class Education(Base):
    __tablename__ = "educations"
    
    id = Column(Integer, primary_key=True, index=True)
    education_level = Column(String)
    institution = Column(String)
    major = Column(String)
    from_year = Column(String)
    to_year = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    candidate = relationship('Candidate', back_populates='educations')
    
class WorkingExperience(Base):
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    from_year = Column(String)
    to_year = Column(String)
    position = Column(String)
    job_description = Column(String)
    salary = Column(Float)
    reasons_resignation = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    candidate = relationship('Candidate', back_populates='experiences')