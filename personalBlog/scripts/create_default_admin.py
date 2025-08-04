from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_utils import hash_password
from app.db import get_db
from app.models import User

ADMIN_EMAIL = "admin@example.com"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"


def create_default_admin():
    """Create a default admin user if no users exist in the database."""
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # Check if any users exist
        stmt = select(User)
        existing_users = db.scalars(stmt).first()

        if existing_users is None:
            # Create admin user with hashed password
            admin_user = User(
                email=ADMIN_EMAIL,
                username=ADMIN_USERNAME,
                password=hash_password(ADMIN_PASSWORD),
            )

            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            print("✅ Default admin user created successfully!")
            print(f"   Email: {ADMIN_EMAIL}")
            print(f"   Username: {ADMIN_USERNAME}")
            print(f"   Password: {ADMIN_PASSWORD}")
        else:
            print("ℹ️  Users already exist in the database. Skipping admin creation.")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    create_default_admin()
