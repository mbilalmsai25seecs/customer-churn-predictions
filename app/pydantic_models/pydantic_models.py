from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Gender(str, Enum):
    FEMALE = "Female"
    MALE = "Male"

class SeniorCitizen(int, Enum):
    NO = 0
    YES = 1

class Partner(str, Enum):
    YES = "Yes"
    NO = "No"

class Dependents(str, Enum):
    NO = "No"
    YES = "Yes"

class PhoneService(str, Enum):
    NO = "No"
    YES = "Yes"

class MultipleLines(str, Enum):
    NO_PHONE_SERVICE = "No phone service"
    NO = "No"
    YES = "Yes"

class InternetService(str, Enum):
    DSL = "DSL"
    FIBER_OPTIC = "Fiber optic"
    NO = "No"

class CommonEnum(str, Enum):
    NO = "No"
    YES = "Yes"
    NO_INTERNET_SERVICE = "No internet service"

class Contract(str, Enum):
    MONTH_TO_MONTH = "Month-to-month"
    ONE_YEAR = "One year"
    TWO_YEAR = "Two year"

class PaperlessBilling(str, Enum):
    YES = "Yes"
    NO = "No"

class PaymentMethod(str, Enum):
    ELECTRONIC_CHECK = "Electronic check"
    MAILED_CHECK = "Mailed check"
    BANK_TRANSFER_AUTOMATIC = "Bank transfer (automatic)"
    CREDIT_CARD_AUTOMATIC = "Credit card (automatic)"

class CustomerChurnPayload(BaseModel):
    gender: Gender
    SeniorCitizen: SeniorCitizen
    Partner: Partner
    Dependents: Dependents
    tenure: int
    PhoneService: PhoneService
    MultipleLines: MultipleLines
    InternetService: InternetService
    OnlineSecurity: CommonEnum
    OnlineBackup: CommonEnum
    DeviceProtection: CommonEnum
    TechSupport: CommonEnum
    StreamingTV: CommonEnum
    StreamingMovies: CommonEnum
    Contract: Contract
    PaperlessBilling: PaperlessBilling
    PaymentMethod: PaymentMethod
    MonthlyCharges: float
    TotalCharges: float
