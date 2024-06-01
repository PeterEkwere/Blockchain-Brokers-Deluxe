from alpaca.data.live.crypto import CryptoDataStream
from config import API_KEY, API_SECRET
from alpaca.broker.client import BrokerClient
from alpaca.broker.requests import CreateAccountRequest, ListAccountsRequest, CreateACHRelationshipRequest, CreateACHTransferRequest
from alpaca.broker.enums import AccountEntities, TaxIdType, FundingSource, AgreementType, BankAccountType, TransferDirection, TransferTiming

from alpaca.broker.models import (
                        Contact,
                        Identity,
                        Disclosures,
                        Agreement
                    )
import datetime
import random
import time

BROKER_API_KEY = 'CK0GUUNOOHMCPXLKJJ6Z'
BROKER_SECRET_KEY = 'PzvO9dGS6cXpgH5V8SVQeYV0VaYcx9t5qiVdxAvj'
broker_client = BrokerClient(
                    api_key=BROKER_API_KEY,
                    secret_key=BROKER_SECRET_KEY,
                    sandbox=True,
                )


def fund_account(ach_relationship):
    """ This Method create and account for a user and funds it

    Returns:
        _type_: _description_
    """
    transfer_data = CreateACHTransferRequest(
                        amount="1000",
                        direction=TransferDirection.INCOMING,
                        timing=TransferTiming.IMMEDIATE,
                        relationship_id=ach_relationship.id
                    )
    transfer = broker_client.create_transfer_for_account(
                    account_id=ach_relationship.account_id,
                    transfer_data=transfer_data
                )

    print(transfer)


def get_all_accounts() -> dict:
    """ This method retrieves all accounts
    """
    filter = ListAccountsRequest(
                    created_after=datetime.datetime.strptime("2022-01-30", "%Y-%m-%d"),
                    entities=[AccountEntities.CONTACT, AccountEntities.IDENTITY]
                    )

    accounts = broker_client.list_accounts(search_parameters=filter)
    return accounts




def create_trading_account(email: str, username: str, phonenumber: str) -> object:
    """ This Method Creates a Trading account for the user
    """
    import random
    Tax_ID = ["444-55-4321", "406-92-2833", "550-06-1732", "558-88-9814", "556-59-2476", "545-28-4725", "565-35-2936"]

    contact_data = Contact(
                email_address=email,
                phone_number=phonenumber,
                street_address=["20 N San Mateo Dr"],
                city="San Mateo",
                state="CA",
                postal_code="94401",
                country="USA"
                )
    # Identity
    identity_data = Identity(
            given_name=username,
            middle_name="Deluxe",
            family_name="TRADING-USER",
            date_of_birth="1990-01-01",
            tax_id=random.choice(Tax_ID),
            tax_id_type=TaxIdType.USA_SSN,
            country_of_citizenship="USA",
            country_of_birth="USA",
            country_of_tax_residence="USA",
            funding_source=[FundingSource.EMPLOYMENT_INCOME]
            )

    # Disclosures
    disclosure_data = Disclosures(
            is_control_person=False,
            is_affiliated_exchange_or_finra=False,
            is_politically_exposed=False,
            immediate_family_exposed=False,
            )

    # Agreements
    agreement_data = [
        Agreement(
        agreement=AgreementType.MARGIN,
        signed_at="2020-09-11T18:09:33Z",
        ip_address="185.13.21.99",
        ),
        Agreement(
        agreement=AgreementType.ACCOUNT,
        signed_at="2020-09-11T18:13:44Z",
        ip_address="185.13.21.99",
        ),
        Agreement(
        agreement=AgreementType.CUSTOMER,
        signed_at="2020-09-11T18:13:44Z",
        ip_address="185.13.21.99",
        ),
        Agreement(
        agreement=AgreementType.CRYPTO,
        signed_at="2020-09-11T18:13:44Z",
        ip_address="185.13.21.99",
        )
    ]

    # ## CreateAccountRequest ## #
    account_data = CreateAccountRequest(
                            contact=contact_data,
                            identity=identity_data,
                            disclosures=disclosure_data,
                            agreements=agreement_data
                            )

    # Make a request to create a new brokerage account
    account = broker_client.create_account(account_data)
    
    time.sleep(2)
    # Create ach relationship for user accoun
    routing_numbers = ["125272865", "146453058", "640651505", "976811967", "706799301", "929488907", "982322071", "091266947"]
    ach_data = CreateACHRelationshipRequest(
                        account_owner_name=account.identity.given_name,
                        bank_account_type=BankAccountType.CHECKING,
                        bank_account_number=account.account_number,
                        bank_routing_number=random.choice(routing_numbers),
                    )

    ach_relationship = broker_client.create_ach_relationship_for_account(
                        account_id=account.id,
                        ach_data=ach_data
                    )
    return ach_relationship


# keys are required for live data
#crypto_stream = CryptoDataStream(API_KEY, API_SECRET)
"""
wss_client = CryptoDataStream()

# async handler
async def quote_data_handler(data):
    # quote data will arrive here
    print(data)

wss_client.subscribe_quotes(quote_data_handler, "BTC")

wss_client.run()
"""

#accounts = get_all_accounts()
#rint(accounts)
achrelationship = create_trading_account("caspr@gmail.com", "caspr", "08038965617")
fund_account(achrelationship)
#print(f"Account id is {account.id}\n Account name is {account.identity.given_name} \n Account Number is {account.account_number}\n")