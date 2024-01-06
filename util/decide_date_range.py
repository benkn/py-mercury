import datetime


class DateRange:
    start_date = datetime.datetime.today()
    end_date = datetime.datetime.today()


def decide_date_range(date):
    """
    Calculates the month date range to use respective to the given date. If the given date is within
    the first four days of the month, then the previous month is used. Else, the current month is used.
    """
    date_range = DateRange()

    # Get last month if the date isn't far enough into this month
    if date.day <= 4:
        date_range.end_date = date.replace(day=1) - datetime.timedelta(days=1)
        date_range.start_date = date.replace(day=1) - datetime.timedelta(
            days=date_range.end_date.day
        )

        # date_range.start_date = start
        # date_range.end_date = end.strftime("%Y-%m-%d")
    else:
        # Else, get the range for this month
        date_range.start_date = date.replace(day=1)  # .strftime("%Y-%m-%d")
        date_range.end_date = date

    # Ensure the type of dates are Date and not DateTime
    date_range.start_date = datetime.date(
        date_range.start_date.year,
        date_range.start_date.month,
        date_range.start_date.day,
    )
    date_range.end_date = datetime.date(
        date_range.end_date.year, date_range.end_date.month, date_range.end_date.day
    )

    print("start", date_range.start_date)
    print("end", date_range.end_date)

    return date_range
