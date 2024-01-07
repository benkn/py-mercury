from util.readable import readable


class TestReadable:
    def test_readable_one(self):
        category = "FOOD_AND_DRINK"
        assert readable(category) == "Food and Drink"

    def test_readable_two(self):
        category = "COFFEE_SHOPS"
        assert readable(category) == "Coffee Shops"

    def test_readable_three(self):
        category = "BOOKS"
        assert readable(category) == "Books"
