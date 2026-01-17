from pydantic import BaseModel, Field

class CarRequest(BaseModel):
    car_model: str
    year: int = Field(ge=1990, le=2026)
    km: int = Field(ge=0)
    fuel: str
    transmission: str
    tax: int = Field(ge=0)
    mpg: float = Field(ge=0)
    engineSize: float = Field(ge=0)
