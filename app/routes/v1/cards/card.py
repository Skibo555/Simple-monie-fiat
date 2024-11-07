from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests
from app.schemas.schemas import AddCard, AddedCardRes
from app.models.models import Card, User
from app.database.database import get_db
from app.oauth.oauth import get_current_user
from helper_functions import get_last_four_num
from typing import List
from visa_credentials.cetificates import load_certificate, load_private_key, user_id, password
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from helper_functions import get_current_time


router = APIRouter(
    tags=["Card"],
    prefix="/api/auth/user"
)


headers = {"Accept": "application/json", "Content-Type": "application/json"}


url = "https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions"

VISA_BASE_FUNDS_TRANSFER_URL = "https://sandbox.api.visa.com/visadirect/fundstransfer"
VISA_PULL_FUNDS_URI = "/v1/pullfundstransactions"

key = load_private_key()
cert = load_certificate()

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)

ACQUIRING_BIN = 408999


def call_vasa_api(card_details: AddCard) -> str:
    pass


@router.post("/add_card", status_code=status.HTTP_201_CREATED, response_model=AddedCardRes)
async def add_card(card_info: AddCard, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    first_name = user.first_name
    last_name = user.last_name
    middle_name = user.middle_name
    city = user.city
    address_line_1 = user.address
    address_line_2 = user.address_2
    postal_code = user.postal_code
    full_pan = card_info.card_number
    last_four_digit = get_last_four_num(full_pan)
    exp_month = card_info.exp_month
    exp_year = card_info.exp_year
    bank_name = card_info.bank_name
    cvv = card_info.cvv
    currency = card_info.currency
    country = card_info.country
    card_type = card_info.card_type
    date_and_time_added = get_current_time()
    alias_type = "to be determined"
    # visa_token = call_vasa_api(card_info)

    payload = {
        "country": f"{country}",
        "recipientLastName": f"{last_name}",
        "recipientMiddleName": f"{middle_name}",
        "city": f"{city}",
        "address2": f"{address_line_2}",
        "recipientFirstName": f"{first_name}",
        "recipientPrimaryAccountNumber": f"{full_pan}",
        "address1": f"{address_line_1}",
        "issuerName": f"{bank_name}",
        "postalCode": f"{postal_code}",
        "cardType": f"{card_type}",
        "consentDateTime": f"{date_and_time_added}",
        "aliasType": f"{alias_type}",
        "cvv": f"{cvv}",
        "guid": "574f4b6a4c2b70472f306f300099515a789092348832455975343637a4d3170",
        "alias": "254711333888"
    }
    
    new_card = Card(
        owner_id=current_user.id,
        last_four_digit=last_four_digit,
        exp_month=exp_month,
        exp_year=exp_year,
        currency=currency,
        country=country
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {
        "message": "You have successfully added your card.",
        "card_details": new_card
    }


@router.get("/get_cards", status_code=status.HTTP_200_OK, response_model=List[AddedCardRes])
async def get_cards(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    cards = db.query(Card).filter(Card.owner_id == current_user.id).all()
    if not cards:
        return {
            "message": "You have no card added to this account.",
            "status_code": status.HTTP_404_NOT_FOUND
        }
    return cards


@router.get("/get_card/{card_id}", status_code=status.HTTP_200_OK, response_model=AddedCardRes)
async def get_one_card(card_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    card = db.query(Card).filter(Card.owner_id == current_user.id).first()
    if not card:
        return {
            "message": "You have no card added to this account.",
            "status_code": status.HTTP_404_NOT_FOUND
        }
    if card.id != card_id:
        return {
            "message": f"You no card with ID {card_id} added to this account.",
            "status_code": status.HTTP_404_NOT_FOUND
        }

    return card

# 'alembic revision --autogenerate -m "Initial migration'

