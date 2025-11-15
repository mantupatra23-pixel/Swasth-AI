# make a backup of existing file just in case
cp app/models/admin.py app/models/admin.py.bak

# overwrite the file with the final content
cat > app/models/admin.py <<'PY'
from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminOut(BaseModel):
    token: str

# Backwards-compatibility: some modules expected a model named `Admin`.
# Provide an alias so `from app.models.admin import Admin` keeps working.
# We prefer to alias to AdminOut (response model). If you actually need
# a DB model, replace this with the correct SQLAlchemy model later.
try:
    Admin = AdminOut
except NameError:
    # Fallback: create a minimal Admin model if AdminOut is not present
    class Admin(BaseModel):
        username: str
        password: str
PY
