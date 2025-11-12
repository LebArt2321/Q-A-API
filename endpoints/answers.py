from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.dependencies import get_db
from models.orm_models import Answer
from models.schemas import Answer as AnswerSchema

router = APIRouter(prefix="/answers", tags=["Answers"])

@router.get("/{id}", response_model=AnswerSchema)  # получить конкретный ответ
def get_answer(id: int, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@router.delete("/{id}") # удалить ответ
def delete_answer(id: int, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(answer)
    db.commit()
    return {"ok": True}