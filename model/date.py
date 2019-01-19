import jpholiday
import datetime


class NotifyDate:
    def __init__(self, datetime: datetime.datetime):
        self.datetime = datetime

    def is_holiday(self) -> bool:
        if self.datetime.weekday == 5 or 6:
            return True
        if jpholiday.is_holiday(self.datetime):
            return True
        return False


