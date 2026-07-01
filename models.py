from database import get_db

# =================================
# AUTH FUNCTIONS
# =================================

def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    db.close()

    return user


def create_user(name, email, password):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """,
        (name, email, password)
    )

    db.commit()
    db.close()


# =================================
# CONTACT CRUD FUNCTIONS
# =================================

def get_all_users():
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM contacts ORDER BY id DESC"
    )

    users = cursor.fetchall()

    db.close()

    return users


def get_user(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM contacts WHERE id = %s",
        (user_id,)
    )

    user = cursor.fetchone()

    db.close()

    return user


def add_user(name, email):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO contacts (name, email)
        VALUES (%s, %s)
        """,
        (name, email)
    )

    db.commit()
    db.close()


def update_user(user_id, name, email):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE contacts
        SET name = %s,
            email = %s
        WHERE id = %s
        """,
        (name, email, user_id)
    )

    db.commit()
    db.close()


def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id = %s",
        (user_id,)
    )

    db.commit()
    db.close()