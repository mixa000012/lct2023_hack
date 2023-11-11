from pydantic.main import BaseModel


class JwtCreate(BaseModel):
    subject: str
    jti: str
    device_id: str
    # expired_time: timedelta
