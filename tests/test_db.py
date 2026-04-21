def test_insert_and_get_latest_price(temp_db):
    temp_db.insert_price(origin="GRU", destination="FLN", price=599.90)

    latest = temp_db.get_latest_price(origin="GRU", destination="FLN")

    assert latest == 599.90


def test_get_latest_price_returns_none_when_empty(temp_db):
    latest = temp_db.get_latest_price(origin="GRU", destination="FLN")
    assert latest is None
