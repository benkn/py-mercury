import datetime
from util.decide_date_range import decide_date_range


class TestDecideDateRange:
    def test_returnsLastMonth(self):
        date = datetime.datetime(2021, 3, 2)
        range = decide_date_range(date)
        assert range.start_date.strftime("%Y-%m-%d") == "2021-02-01"
        assert range.end_date.strftime("%Y-%m-%d") == "2021-02-28"

    def test_returnsThisMonth(self):
        date = datetime.datetime(2021, 2, 8)
        range = decide_date_range(date)
        assert range.start_date.strftime("%Y-%m-%d") == "2021-02-01"
        assert range.end_date.strftime("%Y-%m-%d") == "2021-02-08"

    def test_returnsThisMonthWhole(self):
        date = datetime.datetime(2021, 3, 31)
        range = decide_date_range(date)
        assert range.start_date.strftime("%Y-%m-%d") == "2021-03-01"
        assert range.end_date.strftime("%Y-%m-%d") == "2021-03-31"
