from typing import List, Union

from sqlalchemy.orm import Session, subqueryload
from src.database.models import Contact, User
from src.schemas import ContactModel, ResponseContactModel
from abc import abstractmethod
from sqlalchemy import and_


class BaseContact:

  def __init__(self, db: Session, user: User):
    self.db = db
    self.user = user

  @abstractmethod
  async def __call__(self):
    pass


class Get_Contacts(BaseContact):

  def __init__(self, skip:int, limit:int, db: Session, user: User):
    super().__init__(db, user)
    self.skip = skip
    self.limit = limit

  async def __call__(self) -> List[Contact]:
    return self.db.query(Contact).filter(
      Contact.user_id == self.user.id).offset(self.skip).limit(
        self.limit).all()


class Create_Contact(BaseContact):

  def __init__(self, body, db, user):
    super().__init__(db, user)
    self.body = body

  async def __call__(self) -> Contact:
    new_contact = Contact(
      user_id=self.user.id,
      firstname=self.body.firstname,
      secondname=self.body.secondname,
      email=self.body.email,
      phonenumber=self.body.phonenumber,
      dateofbirth=self.body.dateofbirth,
    )
    self.db.add(new_contact)
    self.db.commit()
    self.db.refresh(new_contact)
    return new_contact


class Get_Contact(BaseContact):

  def __init__(self, contact_id, db, user):
    super().__init__(db, user)
    self.contact_id = contact_id

  async def __call__(self) -> Contact:
    return self.db.query(Contact).filter(
      and_(Contact.id == self.contact_id,
           Contact.user_id == self.user.id)).first()


class Get_Contact_by_Name(BaseContact):

  def __init__(self, contact_name: str, db: Session, user: User):
    super().__init__(db, user)
    self.contact_name = contact_name

  async def __call__(self) -> Contact:
    return self.db.query(Contact).filter(
      and_(Contact.firstname == self.contact_name,
           Contact.user_id == self.user.id)).all()


class Get_Contact_by_Second_Name(BaseContact):

  def __init__(self, contact_name: str, db: Session, user: User):
    super().__init__(db, user)
    self.contact_name = contact_name

  async def __call__(self) -> Contact:
    return self.db.query(Contact).filter(
      and_(Contact.secondname == self.contact_name,
           Contact.user_id == self.user.id)).all()


class Get_Contact_by_Email(BaseContact):

  def __init__(self, email: str, db: Session, user: User):
    super().__init__(db, user)
    self.email = email

  async def __call__(self) -> Contact:
    return self.db.query(Contact).filter(
      and_(Contact.email == self.email,
           Contact.user_id == self.user.id)).all()


class Update_Contact(BaseContact):

  def __init__(self, contact_id, body, db, user):
    super().__init__(db, user)
    self.contact_id = contact_id
    self.body = body

  async def __call__(self) -> Union[Contact, None]:
    contact = self.db.query(Contact).filter(
      and_(Contact.id == self.contact_id,
           Contact.user_id == self.user.id)).first()
    if contact:
      contact.user_id = self.user.id,
      contact.firstname = self.body.firstname,
      contact.secondname = self.body.secondname,
      contact.email = self.body.email,
      contact.phonenumber = self.body.phonenumber,
      contact.dateofbirth = self.body.dateofbirth,
      self.db.commit()
    return contact


class Remove_Contact(BaseContact):

  def __init__(self, contact_id, db, user):
    super().__init__(db, user)
    self.contact_id = contact_id

  async def __call__(self) -> Union[Contact, None]:
    contact = self.db.query(Contact).filter(
      and_(Contact.id == self.contact_id,
           Contact.user_id == self.user.id)).first()
    if contact:
      self.db.delete(contact)
      self.db.commit()
    return contact
