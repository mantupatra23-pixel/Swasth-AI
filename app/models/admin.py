from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminOut(BaseModel):
    token: str

# Backwards compatibility: alias Admin -> AdminOut
# So older imports like `from app.models.admin import Admin` continue to work.
Admin = AdminOut
