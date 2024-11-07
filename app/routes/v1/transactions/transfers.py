import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database.database import Base
from app.oauth.oauth import get_current_user
from generate_number import generate_retrival_reference_num, generate_system_trace_audit_number
from app.database.database import get_db
from visa_credentials.cetificates import load_certificate, load_private_key, user_id, password
from requests_and_responses_code import (
    currency_codes,
    card_type,
    card_subtype,
    card_product_id,
    product_subtype,
)
from requests_and_responses_code.country_codes import load_country_code
from app.schemas.schemas import (
    VisaPushFundsTransfer,
    VisaPullFundsTransfer,
    PointOfServiceData,
    CardAcceptorVisa,
    AddressVerification,
    ServiceProcessingType,
    ColumbiaNationalService,
    RiskAssessmentData
)
from app.models.card import Card
from app.models.user import User


router = APIRouter(
    tags=["Transfers"],
    prefix="api/fiat/transactions"
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
retrival_reference_number = generate_retrival_reference_num()
system_trace_audit_num = generate_system_trace_audit_number()


@router.post("/pull_funds", status_code=status.HTTP_201_CREATED)
async def pull_funds(transaction_details: VisaPullFundsTransfer,
                     current_user: Depends(get_current_user),
                     db: Session = get_db):
    amount_to_send = transaction_details.amount
    user = db.query(User).filter(User.id == current_user.id).first()
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    service_charge = 11.50
    payload_pull = {
        "surcharge": f"{service_charge}",
        "amount": f"{amount_to_send}",
        "localTransactionDateTime": f"{date}",
        "cpsAuthorizationCharacteristicsIndicator": "Y",
        "riskAssessmentData": {
            "traExemptionIndicator": True,
            "trustedMerchantExemptionIndicator": True,
            "scpExemptionIndicator": True,
            "delegatedAuthenticationIndicator": True,
            "lowValueExemptionIndicator": True
        },
        "colombiaNationalServiceData": {
            "addValueTaxReturn": "10.00",
            "taxAmountConsumption": "10.00",
            "nationalNetReimbursementFeeBaseAmount": "20.00",
            "addValueTaxAmount": "10.00",
            "nationalNetMiscAmount": "10.00",
            "countryCodeNationalService": "170",
            "nationalChargebackReason": "11",
            "emvTransactionIndicator": "1",
            "nationalNetMiscAmountType": "A",
            "costTransactionIndicator": "0",
            "nationalReimbursementFee": "20.00"
        },
        "cardAcceptor": {
            "address": {
                "country": "USA",
                "zipCode": "94404",
                "county": "081",
                "state": "CA"
            },
            "idCode": "ABCD1234ABCD123",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "ABCD1234"
        },
        "acquirerCountryCode": 566,
        "acquiringBin": f"{ACQUIRING_BIN}",
        "senderCurrencyCode": "USD",
        "retrievalReferenceNumber": f"{retrival_reference_number}",
        "addressVerificationData": {
            "street": "XYZ St",
            "postalCode": "12345"
        },
        "cavv": "0700100038238906000013405823891061668252",
        "systemsTraceAuditNumber": f"f{system_trace_audit_num}",
        "businessApplicationId": "AA",
        "senderPrimaryAccountNumber": "4060320000000127",
        "settlementServiceIndicator": "9",
        "visaMerchantIdentifier": "73625198",
        "foreignExchangeFeeTransaction": "11.99",
        "senderCardExpiryDate": "2023-10",
        "nationalReimbursementFee": "11.22"
    }
    try:
        r = session.post(
            url=url,
            cert=(cert, key),
            auth=(user_id, password),
            headers=headers,
            timeout=(10, 60),
            json=payload_pull
        )
        r.raise_for_status()
        print(r.json())
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out. The server might be down or unreachable.")
    except requests.exceptions.ReadTimeout:
        print("The server took too long to send the data.")
    except requests.exceptions.ConnectionError as e:
        print(f"A connection error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

    service_charge = 11.50
    payload_push = {
      "surcharge": f"{service_charge}",
      "senderAddress": "901 Metro Center Blvd",
      "pointOfServiceData": {
        "panEntryMode": "90",
        "posConditionCode": "00",
        "motoECIIndicator": "0"
      },
      "recipientPrimaryAccountNumber": "4104920120500001",
      "colombiaNationalServiceData": {
        "addValueTaxReturn": "10.00",
        "taxAmountConsumption": "10.00",
        "nationalNetReimbursementFeeBaseAmount": "20.00",
        "addValueTaxAmount": "10.00",
        "nationalNetMiscAmount": "10.00",
        "countryCodeNationalService": "170",
        "nationalChargebackReason": "11",
        "emvTransactionIndicator": "1",
        "nationalNetMiscAmountType": "A",
        "costTransactionIndicator": "0",
        "nationalReimbursementFee": "20.00"
      },
      "transactionIdentifier": "617020001849971",
      "serviceProcessingType": {
        "requestType": "01"
      },
      "acquiringBin": f"{ACQUIRING_BIN}",
      "retrievalReferenceNumber": "412770451036",
      "systemsTraceAuditNumber": "451018",
      "senderName": f"{user.last_name.title(), user.first_name, user.middle_name}",
      "businessApplicationId": "AA",
      "settlementServiceIndicator": "9",
      "transactionCurrencyCode": "USD",
      "recipientName": "rohan",
      "sourceAmount": "123.12",
      "senderCountryCode": "124",
      "senderAccountNumber": "4104920120500002",
      "amount": "124.05",
      "localTransactionDateTime": "2023-05-05T12:00:00",
      "purposeOfPayment": "purpose",
      "cardAcceptor": {
        "address": {
          "country": "USA",
          "zipCode": "94404",
          "county": "San Mateo",
          "state": "CA"
        },
        "idCode": "CA-IDCode-77765",
        "name": "Visa Inc. USA-Foster City",
        "terminalId": "TID-9999"
      },
      "senderReference": "",
      "acquirerCountryCode": "840",
      "sourceCurrencyCode": "840",
      "senderCity": "Foster City",
      "senderStateCode": "CA",
      "merchantCategoryCode": "6012",
      "sourceOfFundsCode": "05"
    }

    try:
        r = session.post(
            url=url,
            cert=(cert, key),
            auth=(user_id, password),
            headers=headers,
            timeout=(10, 60),
            json=payload_push
        )
        r.raise_for_status()
        print(r.json())
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out. The server might be down or unreachable.")
    except requests.exceptions.ReadTimeout:
        print("The server took too long to send the data.")
    except requests.exceptions.ConnectionError as e:
        print(f"A connection error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

