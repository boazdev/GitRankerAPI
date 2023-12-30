from typing import Optional
from sqlalchemy.orm import Session
from app.models.user_code_data_model import UserCodeData

from app.schemas.programming_langs_schema import UserLinesCode

def create_user_code(db: Session, user_code: UserLinesCode) -> Optional[UserLinesCode]:
    try:
        db_user = db.query(UserCodeData).filter(UserCodeData.users_metadata_id == user_code.users_metadata_id).first()
        if db_user:
            # Update the existing user_code
            for key, value in user_code.model_dump().items():
                setattr(db_user, key, value)
        else:
            # Create a new user_code
            db_user = UserCodeData(**user_code.model_dump())
            db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f'sql exception: {e}')
        db.rollback()
        raise