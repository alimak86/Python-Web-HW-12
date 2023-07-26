from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.database import Connect_db, SQLALCHEMY_DATABASE_URL_FOR_WORK
from src.schemas import ContactModel, ResponseContactModel, ContactModelFullName
from src.repository import contacts as repository_contacts
from src.database.models import User
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])
"""
extract all contacts
"""


@router.get("/", response_model=List[ResponseContactModel])
async def read_contacts(
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Get_Contacts(skip, limit, db, current_user)
  contacts = await execute()
  output = []
  for contact in contacts:
    output.append(ResponseContactModel(id = contact.id, 
                                       firstname = contact.firstname, 
                                       secondname = contact.secondname,
                                       email = contact.email,
                                         phonenumber = contact.phonenumber, 
                                         dateofbirth=contact.dateofbirth))
  return output


"""
find contacts with the specified first name
"""


@router.get("/name/{firstname}",response_model = List[ContactModel])
async def read_contact_by_name(
  firstname: str,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Get_Contact_by_Name(firstname, db,
                                                    current_user)
  contacts = await execute()

  if contacts is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Contact not found")
  output = []
  for contact in contacts:
    output.append(ContactModel(firstname = contact.firstname, 
                               secondname = contact.secondname,
                               email = contact.email, 
                               phonenumber = contact.phonenumber, 
                               dateofbirth=contact.dateofbirth))
  return output


#  return firstname
"""
find contacts with the specified second name
"""


@router.get("/secondname/{secondname}",response_model =List[ContactModel])
async def read_contact_by_secondname(
  secondname: str,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Get_Contact_by_Second_Name(
    secondname, db, current_user)
  contacts = await execute()

  if contacts is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Contact not found")
  output = []
  for contact in contacts:
    output.append(ContactModel(firstname = contact.firstname, 
                               secondname = contact.secondname,
                               email = contact.email, 
                               phonenumber = contact.phonenumber, 
                               dateofbirth=contact.dateofbirth))
  return output


"""
find contacts with the specified email
"""


@router.get("/email/{email}",response_model = List[ContactModel])
async def read_contact_by_name(
  email: str,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Get_Contact_by_Email(email, db, current_user)
  contacts = await execute()

  if contacts is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Contact not found")
  output = []
  for contact in contacts:
    output.append(ContactModel(firstname = contact.firstname, 
                               secondname = contact.secondname,
                               email = contact.email, 
                               phonenumber = contact.phonenumber, 
                               dateofbirth=contact.dateofbirth))
  return output


"""
extract contact defined by id
"""


@router.get("/{contact_id}", response_model=ContactModelFullName)
async def read_contact(
  contact_id: int,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Get_Contact(contact_id, db, current_user)
  contact = await execute()
  if contact is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Contact not found")
  return ContactModelFullName(firstname = contact.firstname, 
                               secondname = contact.secondname)


"""
create new contact
"""


@router.post("/", response_model=ResponseContactModel)
async def create_contact(
  body: ContactModel,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Create_Contact(body, db, current_user)
  contact = await execute()
  
  return ResponseContactModel(id = contact.id, 
                                       firstname = contact.firstname, 
                                       secondname = contact.secondname,
                                       email = contact.email,
                                         phonenumber = contact.phonenumber, 
                                         dateofbirth=contact.dateofbirth)


"""
update contact info
"""


@router.put("/{contact_id}", response_model=ResponseContactModel)
async def update_contact(
  body: ContactModel,
  contact_id: int,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Update_Contact(contact_id, body, db,
                                               current_user)
  contact = await execute()
  if contact is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Contact not found")
  return ResponseContactModel(id = contact.id, 
                                       firstname = contact.firstname, 
                                       secondname = contact.secondname,
                                       email = contact.email,
                                         phonenumber = contact.phonenumber, 
                                         dateofbirth=contact.dateofbirth)


"""
remove contact with the specified id
"""


@router.delete("/{contact_id}", response_model=ResponseContactModel)
async def remove_contact(
  contact_id: int,
  db: Session = Depends(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK)),
  current_user: User = Depends(auth_service.get_current_user)):
  execute = repository_contacts.Remove_Contact(contact_id, db, current_user)
  contact = await execute()
  if contact is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Contact not found")
  return ResponseContactModel(id = contact.id, 
                                       firstname = contact.firstname, 
                                       secondname = contact.secondname,
                                       email = contact.email,
                                         phonenumber = contact.phonenumber, 
                                         dateofbirth=contact.dateofbirth)
