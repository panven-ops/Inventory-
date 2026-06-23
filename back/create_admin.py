import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from repo/repo_users import get_user_by_username, update_user

def make_admin(username: str):
    db SessionLocal()

    try:
        user = get_user_by_username(db, username)

        if not user:
            print(f"User '{username}' not found")
            return

        if user.is_admin:
            print(f"User '{username}' is already admin")
            return

        user.is_admin = True
        update_user(db, user)
        print(f"User '{username}' is an admin from now")

    finally:
        db.close()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python create_admin.py <username>")
        sys.exit(1)

    make_admin(sys.argv[1])
