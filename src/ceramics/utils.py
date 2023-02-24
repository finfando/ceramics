from datetime import date, timedelta


def weekly_date_range(start_date: date, end_date: date, weekday: int):
    for n in range(int((end_date - start_date).days)):
        day = start_date + timedelta(n)
        if day.weekday() == weekday:
            yield day
