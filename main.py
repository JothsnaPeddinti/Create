from fastapi import FastAPI, Depends,UploadFile, File, Form, HTTPException
from typing import Annotated,List,Optional
from pathlib import Path
import uuid
import shutil
import os
import pathlib
from fastapi import File, UploadFile,Form
from sqlalchemy.orm import Session
from database import engine,get_db
import models
import schemas
from database import SessionLocal,Base
from schemas import BulkEmailCreate, EmailResponse
from models import Email
from datetime import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def db_dependency():
        db=SessionLocal()
        try:
                yield db
        finally:
                db.close()        





@app.post("/email",response_model=schemas.EmailResponse,status_code=201)
def create_email(email:schemas.EmailCreate, db: Session = Depends(get_db)):
    db_email=models.Email(from_address=email.from_address,to_address=email.to_address,subject=email.subject,body=email.body,attachment_path=email.attachment_path,appname=email.appname,feature=email.feature,priority=email.priority)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

@app.post("/e-mail-attachment")
async def create_email_with_attachment(from_address: str =Form(...),to_address: str =Form(...),subject: str =Form(...),body: str =Form(...),attachment: UploadFile= File(None),db: db_dependency=Depends()):
                                      file_path=None
                                      if attachment:
                                              file_path= f"uploads/{attachment.filename}"
                                              with open(file_path,"wb") as f:
                                                      f.write(await attachment.read())
                                      new_email=models.Email(from_address=from_address,
                                                             to_address=to_address,
                                                             subject=subject,
                                                             body=body,
                                                             attachment_path=file_path)                
                                      db.add(new_email)
                                      db.commit()
                                      db.refresh(new_email)
                                      return{"message":"Email saved","email_id": new_email.id}

@app.get("/emails",response_model=list[schemas.EmailResponse])
def get_all_emails(db: Session=Depends(get_db)):
        emails=db.query(models.Email).all()
        return emails

@app.post("/email-attachment")
async def create_email_with_attachment(
    from_address: str =Form(...),
    to_address: str =Form(...),
    subject: str =Form(...),
    body: str =Form(...),
    attachment: UploadFile = File(None),
    appname: str = Form(...),
    feature: str =Form(...),
    priority: str =Form(...),

    db: Session =Depends(get_db)
):
                                

    file_path=None
    if attachment:
            
            upload_dir=Path("Uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            ext = Path(attachment.filename).suffix
            dest = upload_dir / f"{uuid.uuid4().hex}{ext}"

            with dest.open("wb") as buffer:
              shutil.copyfileobj(attachment.file,buffer)

              file_path= str(dest)

    new_email = models.Email(from_address=from_address,
                         to_address=to_address,
                         subject=subject,
                         body=body,
                         attachment_path=file_path,
                         appname=appname,
                         feature=feature,
                         priority=priority
                         )
    db.add(new_email)
    db.commit()  
    db.refresh(new_email)

    return{
        "message": "Email + attachment stored successfully",
        "id": new_email.id,
        "attachment_path": new_email.attachment_path
        
        }
@app.post("/email/bulk",response_model=list[EmailResponse])
def create_bulk_emails(data:BulkEmailCreate,db: Session =Depends(get_db)):
        email_objects=[Email(from_address=e.from_address,
                             to_address=e.to_address,
                             subject=e.subject,
                             body=e.body,
                             attachment_path=e.attachment_path,
                             appname=e.appname,
                             feature=e.feature,
                             priority=e.priority,
                             created_at=datetime.utcnow(),
                             updated_at=datetime.utcnow()
                             )
                             for e in data.emails
                             ]
        db.bulk_save_objects(email_objects)
        db.commit()
        return  [
            EmailResponse(id=e.id,
                           from_address=e.from_address,
                           to_address=e.to_address,
                           subject=e.subject,
                           body=e.body,
                           attachment_path=e.attachment_path,
                           appname=e.appname,
                           feature=e.feature,
                           priority=e.priority,
                           created_at=e.created_at,
                           updated_at=e.updated_at,
            )
            for e in email_objects

        ]
            


                
                                