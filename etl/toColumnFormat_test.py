from etl.toColumnFormat import headerRow, to_columns


class TestToColumnFormat:
    def test_headerRow(self):
        assert len(headerRow) == 9

    def test_to_columns(self):
        transaction = {
            "date": "2023-12-13",
            "name": "Whole Foods",
            "amount": 100,
            "my_category": "Food and Drink",
            "my_sub_category": "Groceries",
            "account_owner": "First Platypus",
            "my_raw_category": "FOOD_AND_DRINK_GROCERIES",
            "transaction_id": "12321",
        }

        results = to_columns([transaction])
        assert len(results) == 1
        assert len(results[0]) == 9
        assert results[0][0] == "2023-12-13"
        assert results[0][1] == "Whole Foods"
        assert results[0][2] == 100
        assert results[0][3] == ""
        assert results[0][4] == "Food and Drink"
        assert results[0][5] == "Groceries"
        assert results[0][6] == "First Platypus"
        assert results[0][7] == "FOOD_AND_DRINK_GROCERIES"
        assert results[0][8] == "12321"

    def test_multiple_to_columns(self):
        transaction = {
            "date": "2023-12-13",
            "name": "Whole Foods",
            "amount": 100,
            "my_category": "Food and Drink",
            "my_sub_category": "Groceries",
            "account_owner": "First Platypus",
            "my_raw_category": "FOOD_AND_DRINK_GROCERIES",
            "transaction_id": "12321",
        }

        results = to_columns([transaction, transaction, transaction])
        assert len(results) == 3
