from fastapi import FastAPI, HTTPException
from faker import Faker
from uuid import uuid4
from datetime import datetime
import random
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()
fake = Faker()

# ----- Your schemas (simplified for example) -----


class Wallet(BaseModel):
    id: str
    wallet_number: str
    wallet_name: str
    currency: str
    wallet_type: str
    wallet_logo: str = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None


class Category(BaseModel):
    id: str
    name: str
    description: str
    icon_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class Transaction(BaseModel):
    id: str
    wallet_id: str
    category_id: str
    currency: str
    amount: float
    note: str
    transaction_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None


# ----- In-memory "database" for demo -----
wallets_db = []
categories_db = []
transactions_db = []

# ----- Constants -----
ACCOUNT_TYPES = ["ABA", "WING", "AC", "CASH"]
CURRENCIES = ["USD", "KHR"]
CATEGORY_EXAMPLES = [
    {"name": "Food & Drinks", "description": "Meals, coffee, snacks", "icon_name": "restaurant"},
    {"name": "Sports", "description": "Gym, fitness, sports activities", "icon_name": "fitness_center"},
    {"name": "Utilities", "description": "Electricity, water, internet bills", "icon_name": "flash_on"},
    {"name": "Health", "description": "Medical, pharmacy", "icon_name": "local_hospital"},
    {"name": "Salary", "description": "Monthly income", "icon_name": "attach_money"},
    {"name": "Transfers", "description": "Money moved between wallets", "icon_name": "swap_horiz"},
]

# ----- Data generation functions -----


def generate_wallet() -> Wallet:
    return Wallet(
        id=str(uuid4()),
        wallet_number=fake.bothify(text='??##??##'),
        wallet_name=fake.company(),
        currency=random.choice(CURRENCIES),
        wallet_type=random.choice(ACCOUNT_TYPES),
        is_active=True,
        created_at=fake.date_time_between(start_date='-2y', end_date='now'),
        updated_at=None,
    )


def generate_category() -> Category:
    cat = random.choice(CATEGORY_EXAMPLES)
    return Category(
        id=str(uuid4()),
        name=cat["name"],
        description=cat["description"],
        icon_name=cat["icon_name"],
        created_at=fake.date_time_between(start_date='-2y', end_date='now'),
        updated_at=None,
    )


def generate_transaction(wallet: Wallet, category: Category) -> Transaction:
    trans_date = fake.date_time_between(start_date='-90d', end_date='now')
    amount = round(random.uniform(5, 500), 2)

    return Transaction(
        id=str(uuid4()),
        wallet_id=wallet.id,
        category_id=category.id,
        currency=wallet.currency,
        amount=abs(amount),
        note=fake.sentence(nb_words=6),
        transaction_date=trans_date,
        created_at=trans_date,
        updated_at=None,
    )

# ----- API endpoints -----


@app.post("/seed/wallets", response_model=List[Wallet])
def seed_wallets(count: int = 5):
    new_wallets = [generate_wallet() for _ in range(count)]
    wallets_db.extend(new_wallets)
    return new_wallets


@app.post("/seed/categories", response_model=List[Category])
def seed_categories():
    # Seed one of each example category only
    new_categories = [Category(**cat) for cat in [
        {
            "id": str(uuid4()),
            "name": c["name"],
            "description": c["description"],
            "icon_name": c["icon_name"],
            "created_at": datetime.utcnow(),
            "updated_at": None,
        } for c in CATEGORY_EXAMPLES
    ]]
    categories_db.extend(new_categories)
    return new_categories


@app.post("/seed/transactions", response_model=List[Transaction])
def seed_transactions(count: int = 50):
    if not wallets_db or not categories_db:
        raise HTTPException(
            status_code=400, detail="Seed wallets and categories first")

    new_transactions = []
    for _ in range(count):
        wallet = random.choice(wallets_db)
        category = random.choice(categories_db)
        trans = generate_transaction(wallet, category)
        new_transactions.append(trans)

    transactions_db.extend(new_transactions)
    return new_transactions


@app.get("/wallets", response_model=List[Wallet])
def list_wallets():
    return wallets_db


@app.get("/categories", response_model=List[Category])
def list_categories():
    return categories_db


@app.get("/transactions", response_model=List[Transaction])
def list_transactions():
    return transactions_db


def seed_all():
    # call your generate_wallet, generate_category, generate_transaction
    # save to DB or whatever persistence you use
    pass


if __name__ == "__main__":
    seed_all()
