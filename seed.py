"""Seed the database with an initial dispatcher account and sample data.

Run after applying migrations:

    python seed.py
"""
from app.core.database import SessionLocal
from app.core.logging_config import get_logger
from app.models import Specialist, User
from app.core.security import hash_password

logger = get_logger("seed")


def run() -> None:
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "dispatcher").first():
            db.add(
                User(
                    username="dispatcher",
                    full_name="Іван Диспетчер",
                    hashed_password=hash_password("dispatcher123"),
                    role="dispatcher",
                )
            )
        if not db.query(User).filter(User.username == "tenant").first():
            db.add(
                User(
                    username="tenant",
                    full_name="Олена Квартиронаймач",
                    hashed_password=hash_password("tenant123"),
                    role="tenant",
                )
            )
        if db.query(Specialist).count() == 0:
            db.add_all(
                [
                    Specialist(full_name="Петро Електрик", specialty="electrical"),
                    Specialist(full_name="Сергій Сантехнік", specialty="plumbing"),
                    Specialist(full_name="Микола Майстер", specialty="general"),
                ]
            )
        db.commit()
        logger.info("Seed data created (users: dispatcher/dispatcher123, tenant/tenant123)")
    finally:
        db.close()


if __name__ == "__main__":
    run()
