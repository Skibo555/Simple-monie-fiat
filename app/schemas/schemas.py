from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserRegisterForm(BaseModel):
    username: str
    first_name: str
    last_name: str
    middle_name: str = None
    country: str
    city: str
    email: EmailStr
    password: str
    address: str
    address_2: str = None
    postal_code: str

    class Config:
        from_attributes=True


class UserLoginForm(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes=True


class AuthResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes=True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes=True


class TokenData(BaseModel):
    id: Optional[int] = None
    user_email: EmailStr
    username: str

    class Config:
        from_attributes=True


class ForgetPasswordRequest(BaseModel):
    email: EmailStr


class ResetForgetPassword(BaseModel):
    new_password: str
    confirm_password: str


class SuccessMessageResetPassword(BaseModel):
    success: bool
    status_code: int
    message: str


class AddCard(BaseModel):
    card_number: str
    exp_month: str
    exp_year: str
    cvv: str
    bank_name: str
    card_type: str
    currency: str = "NGN"
    country: str = "Nigeria"


class AddedCardRes(BaseModel):
    card_number: str
    exp_month: str
    exp_year: str


class CardAcceptorAddress(BaseModel):
    country: str
    zipCode: str
    county: str
    state: str


class CardAcceptorVisa(BaseModel):
    address: CardAcceptorAddress
    idCode: str
    name: str
    terminalId: str


class RiskAssessmentData(BaseModel):
    tranExemptionIndicator: bool
    trustedMerchantExemptionIndication: bool
    scpExemptionIndicator: bool
    delegatedAuthenticationIndicator: bool
    lowValueExemptionIndicator: bool


class ColumbiaNationalService(BaseModel):
    addValueTaxReturn: float
    taxAmountConsumption: float
    nationalNetReimbursementFeeBaseAmount: float
    addValueTaxAmount: float
    nationalNetMiscAmount: float
    countryCodeNationalService: float
    nationalChargebackReason: float
    emvTransactionIndicator: int
    nationalNetMiscAmountType: str
    costTransactionIndicator: float
    nationalReimbursementFee: float


class AddressVerification(BaseModel):
    street: str
    postalCode: int


class VisaPullFundsTransfer(BaseModel):
    amount: float
    recipient_pan: int


class PointOfServiceData(BaseModel):
    panEntryMode: int
    posConditionalCode: int
    motoECIIndicator: int


class ServiceProcessingType(BaseModel):
    requestType: int


class VisaPushFundsTransfer(BaseModel):
    surcharge: float
    senderAddress: str
    recipientPrimaryAccountNumber: int
    colombiaNationalServiceData: ColumbiaNationalService
    transactionIdentifier: int
    acquiringBin: int
    retrievalReferenceNumber: int
    systemsTraceAuditNumber: int
    senderName: str
    businessApplicationId: str
    settlementServiceIndicator: int
    transactionCurrencyCode: str
    recipientName: str
    sourceAmount: float
    senderCountryCode: int
    senderAccountNumber: int
    amount: float
    localTransactionDateTime: str
    purposeOfPayment: str
    cardAcceptor: CardAcceptorVisa
    senderReference: str
    acquirerCountryCode: int
    sourceCurrencyCode: int
    senderCity: str
    senderStateCode: str
    merchantCategoryCode: int
    sourceOfFundsCode: int

