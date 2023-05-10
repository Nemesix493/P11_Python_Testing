import datetime


def string_to_datetime(string: str) -> datetime.datetime:
    date_time = string.split(' ')
    date = date_time[0].split('-')
    time = date_time[1].split(':')
    return datetime.datetime(
        *[
            *[int(value) for value in date],
            *[int(value) for value in time]
        ]
    )
