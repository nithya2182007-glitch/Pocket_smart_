from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3,max_length=40)
    password: str = Field(min_length=6,max_length=100)

class LoginRequest(BaseModel):
    username: str
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    rooms: list[str] = Field(min_length=1)
    items: dict[str,int] = {}
    style: str = "Modern"
    notes: str = ""

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0)
    event_type: str = "Birthday"
    venue: str = "Home"
    city: str = ""
    notes: str = ""

class TravelRequest(BaseModel):
    budget: float = Field(gt=0)
    destination: str = Field(min_length=2, max_length=100)
    days: int = Field(gt=0, le=60)
    travelers: int = Field(gt=0, le=30)
    travel_style: str = "Balanced"
    transport: str = "Any"
    notes: str = ""

class MealRequest(BaseModel):
    budget: float = Field(gt=0)
    people: int = Field(gt=0, le=100)
    days: int = Field(gt=0, le=31)
    cuisine: str = "Any"
    dietary_preferences: str = "None"
    notes: str = ""

class ShoppingRequest(BaseModel):
    budget: float = Field(gt=0)
    category: str = "General"
    items: list[str] = Field(min_length=1, max_length=30)
    priority: str = "Best value"
    notes: str = ""
