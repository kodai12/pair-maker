from lambdalayer import jpholiday
import datetime

from model.value import Value


class NotifyDate(Value):
    def __init__(self, datetime: datetime.datetime):
        self.datetime = datetime

    def is_holiday(self) -> bool:
        if self.datetime.weekday() == 5 or self.datetime.weekday() == 6:
            return True
        if jpholiday.is_holiday(self.datetime.date()):
            return True
        return False

    def get_weekday(self) -> int:
        return self.datetime.weekday()

