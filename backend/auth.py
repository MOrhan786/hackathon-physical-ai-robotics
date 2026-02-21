import os
import uuid
import json
import hashlib
import hmac
from datetime import datetime, timedelta, timezone

import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_URL = os.getenv("DATABASE_URL", "")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")


def get_db_connection():
    """Get a new database connection."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """Create tables if they don't exist."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    background JSONB DEFAULT '{}',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMPTZ NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            # Index for fast token lookups
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
            """)
            conn.commit()
            print("Database tables initialized successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Database init error: {e}")
        raise
    finally:
        conn.close()


def _generate_session_token() -> str:
    """Generate a secure session token using Better Auth secret."""
    raw = f"{uuid.uuid4()}-{datetime.now(timezone.utc).isoformat()}"
    token = hmac.new(
        BETTER_AUTH_SECRET.encode(),
        raw.encode(),
        hashlib.sha256
    ).hexdigest()
    return token


def signup(email: str, password: str, name: str, background: dict) -> dict:
    """Create a new user account and return user + session token."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Check if email already exists
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                raise ValueError("Email already registered")

            # Hash password with bcrypt
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            # Create user
            user_id = str(uuid.uuid4())
            cur.execute(
                """INSERT INTO users (id, email, name, password_hash, background)
                   VALUES (%s, %s, %s, %s, %s)""",
                (user_id, email, name, password_hash, json.dumps(background))
            )

            # Create session
            session_id = str(uuid.uuid4())
            token = _generate_session_token()
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)
            cur.execute(
                """INSERT INTO sessions (id, user_id, token, expires_at)
                   VALUES (%s, %s, %s, %s)""",
                (session_id, user_id, token, expires_at)
            )

            conn.commit()

            return {
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": name,
                    "background": background,
                },
                "session_token": token,
            }
    except ValueError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise Exception(f"Signup failed: {e}")
    finally:
        conn.close()


def signin(email: str, password: str) -> dict:
    """Authenticate user and return user + session token."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Find user by email
            cur.execute(
                "SELECT id, email, name, password_hash, background FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()
            if not user:
                raise ValueError("Invalid email or password")

            # Verify password
            if not bcrypt.checkpw(
                password.encode("utf-8"),
                user["password_hash"].encode("utf-8")
            ):
                raise ValueError("Invalid email or password")

            # Create new session
            session_id = str(uuid.uuid4())
            token = _generate_session_token()
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)
            cur.execute(
                """INSERT INTO sessions (id, user_id, token, expires_at)
                   VALUES (%s, %s, %s, %s)""",
                (session_id, user["id"], token, expires_at)
            )
            conn.commit()

            background = user["background"]
            if isinstance(background, str):
                background = json.loads(background)

            return {
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "background": background,
                },
                "session_token": token,
            }
    except ValueError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise Exception(f"Signin failed: {e}")
    finally:
        conn.close()


def signout(session_token: str) -> bool:
    """Invalidate a session by deleting it."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM sessions WHERE token = %s", (session_token,))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        print(f"Signout error: {e}")
        return False
    finally:
        conn.close()
