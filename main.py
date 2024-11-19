'''from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List,Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text:str
    is_correct:bool

class QuestionBase(BaseModel):
    question_text:str
    choices: List[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/questions/{question_id")
async def read_questions(question_id: int, db:db_dependency):
    result =db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException (status_code = 404, detail= 'Choices is not found')
    return result


@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()'''

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Pydantic models
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# --- GET all questions ---
@app.get("/questions/", response_model=List[QuestionBase])
async def get_all_questions(db: db_dependency):
    result = db.query(models.Questions).all()
    return result


# --- GET a specific question by ID ---
@app.get("/questions/{question_id}", response_model=QuestionBase)
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result


# --- GET choices for a specific question ---
@app.get("/choices/{question_id}", response_model=List[ChoiceBase])
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result


# --- POST a new question ---
@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Add choices associated with this question
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct,
                                   question_id=db_question.id)
        db.add(db_choice)

    db.commit()
    return db_question


# --- PUT (Update) a specific question ---
@app.put("/questions/{question_id}")
async def update_question(question_id: int, question: QuestionBase, db: db_dependency):
    db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    db_question.question_text = question.question_text
    db.commit()
    db.refresh(db_question)

    # Update choices associated with this question
    for choice in question.choices:
        db_choice = db.query(models.Choices).filter(models.Choices.question_id == question_id).first()
        if db_choice:
            db_choice.choice_text = choice.choice_text
            db_choice.is_correct = choice.is_correct
        else:
            db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct,
                                       question_id=db_question.id)
            db.add(db_choice)

    db.commit()
    return db_question


# --- DELETE a specific question ---
@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Delete all choices associated with this question
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    db.commit()  # Commit deletion of choices

    # Delete the question itself
    db.delete(db_question)
    db.commit()  # Commit deletion of the question

    return {"message": "Question deleted successfully"}


# --- PUT (Update) a specific choice ---
@app.put("/choices/{choice_id}")
async def update_choice(choice_id: int, choice: ChoiceBase, db: db_dependency):
    db_choice = db.query(models.Choices).filter(models.Choices.id == choice_id).first()
    if not db_choice:
        raise HTTPException(status_code=404, detail="Choice not found")

    db_choice.choice_text = choice.choice_text
    db_choice.is_correct = choice.is_correct
    db.commit()  # Commit changes
    db.refresh(db_choice)  # Refresh to get the updated data

    return db_choice  # Return the updated choice


# --- DELETE a specific choice ---
@app.delete("/choices/{choice_id}")
async def delete_choice(choice_id: int, db: db_dependency):
    db_choice = db.query(models.Choices).filter(models.Choices.id == choice_id).first()
    if not db_choice:
        raise HTTPException(status_code=404, detail="Choice not found")

    # Delete the choice
    db.delete(db_choice)
    db.commit()  # Commit the deletion

    return {"message": "Choice deleted successfully"}

