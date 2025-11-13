from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.dependencies import get_db
from models.orm_models import Question, Answer
from models.schemas import Answer as AnswerSchema, Question as QuestionSchema, QuestionCreate, QuestionList, AnswerCreate

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/", response_model=list[QuestionList])  # список всех вопросов
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions

@router.post("/", response_model=QuestionSchema) # создать новый вопрос
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/{id}", response_model=QuestionSchema)  # получить вопрос и все ответы
def get_question_with_answers(id: int, db: Session = Depends(get_db)):
    question = (
        db.query(Question)
        .options(joinedload(Question.answers))
        .filter(Question.id == id)
        .first()
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.delete("/{id}") # удалить вопрос (вместе с ответами)
def delete_question(id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"ok": True}

@router.post("/{id}/answers", response_model=AnswerSchema) # добавить ответ к вопросу
def add_answer(answer: AnswerCreate, id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_answer = Answer(**answer.model_dump(), question_id=id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer
