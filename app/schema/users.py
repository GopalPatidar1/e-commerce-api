from pydantic import BaseModel, field_validator, ConfigDict, Field, EmailStr

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    status: str | None = None


class CreateUser(BaseModel):
    firstname: str = Field(min_length=3, max_length=10)
    lastname: str
    email: EmailStr
    password: str

    # This forbids any extra fields in the request
    model_config = ConfigDict(extra="forbid")

    @field_validator("lastname")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Firstname and lastname must be at least 3 characters long")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value