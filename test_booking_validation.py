from sqlalchemy import create_engine, text
import pytest

DB_URL = "mysql+pymysql://root:@localhost/ayo"   # sesuaikan username/password
engine = create_engine(DB_URL)


def test_double_booking():
    query = text("""
        SELECT b1.id AS booking1_id, b2.id AS booking2_id
        FROM t_booking b1
        JOIN t_booking b2
            ON b1.venue_id = b2.venue_id
            AND b1.date = b2.date
            AND b1.id <> b2.id
            AND b1.start_time < b2.end_time
            AND b2.start_time < b1.end_time;
    """)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    assert len(result) == 0, f"Double booking detected: {result}"


def test_wrong_price():
    query = text("""
        SELECT b.id, b.price, p.price AS correct_price
        FROM t_booking b
        JOIN t_price p
            ON b.venue_id = p.venue_id
            AND b.date = p.date
            AND b.start_time = p.start_time
            AND b.end_time = p.end_time
        WHERE b.price <> p.price;
    """)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    assert len(result) == 0, f"Incorrect booking price detected: {result}"
