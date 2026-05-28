"""台電離峰日與夏月判斷."""

from datetime import date, datetime

try:
    from lunar_python import Lunar

    HAS_LUNAR = True
except ImportError:
    HAS_LUNAR = False


def is_summer(dt: datetime) -> bool:
    return 6 <= dt.month <= 9


def is_holiday(dt: datetime) -> bool:
    if is_holiday_simple(dt):
        return True

    lunar_date = None
    if HAS_LUNAR:
        try:
            lunar_date = Lunar.fromDate(datetime(dt.year, dt.month, dt.day))
        except Exception:
            pass

    if _is_western_holiday(dt):
        return True

    if lunar_date and _is_lunar_holiday(lunar_date):
        return True

    return False


def _is_western_holiday(dt: datetime) -> bool:
    if dt.month == 1 and dt.day == 1:
        return True
    if dt.month == 2 and dt.day == 28:
        return True
    if dt.month == 4 and dt.day == 4:
        return True
    if dt.month == 4 and dt.day == 5:
        return True
    if dt.month == 5 and dt.day == 1:
        return True
    if dt.month == 9 and dt.day == 28:
        return True
    if dt.month == 10 and dt.day == 10:
        return True
    if dt.month == 10 and dt.day == 25:
        return True
    if dt.month == 12 and dt.day == 25:
        return True
    return False


def _is_lunar_holiday(lunar_date) -> bool:
    if not lunar_date:
        return False

    month = lunar_date.getMonth()
    day = lunar_date.getDay()

    if month == 1 and 1 <= day <= 5:
        return True
    if month == 5 and day == 5:
        return True
    if month == 8 and day == 15:
        return True

    return False


def is_lunar_new_year_eve(dt: datetime) -> bool:
    if not HAS_LUNAR:
        return False

    try:
        lunar_date = Lunar.fromDate(datetime(dt.year, dt.month, dt.day))
        return lunar_date.getMonth() == 12
    except Exception:
        return False


OFF_PEAK_DAYS = {
    2024: {
        (1, 1), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 28),
        (4, 4), (4, 5), (5, 1), (6, 10), (9, 17), (9, 28), (10, 10), (10, 25), (12, 25),
    },
    2025: {
        (1, 1), (1, 28), (1, 29), (1, 30), (1, 31), (2, 1), (2, 28),
        (4, 4), (4, 5), (5, 1), (5, 31), (9, 28), (10, 6), (10, 10), (10, 25), (12, 25),
    },
    2026: {
        (1, 1), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 28),
        (4, 4), (4, 5), (5, 1), (6, 19), (9, 25), (9, 28), (10, 10), (10, 25), (12, 25),
    },
    2027: {
        (1, 1), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 28),
        (4, 4), (4, 5), (5, 1), (6, 9), (9, 15), (9, 28), (10, 10), (10, 25), (12, 25),
    },
    2028: {
        (1, 1), (1, 26), (1, 27), (1, 28), (1, 29), (1, 30), (2, 28),
        (4, 4), (4, 5), (5, 1), (5, 28), (9, 28), (10, 3), (10, 10), (10, 25), (12, 25),
    },
    2029: {
        (1, 1), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 28),
        (4, 4), (4, 5), (5, 1), (6, 16), (9, 22), (9, 28), (10, 10), (10, 25), (12, 25),
    },
    2030: {
        (1, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 28),
        (4, 4), (4, 5), (5, 1), (6, 5), (9, 12), (9, 28), (10, 10), (10, 25), (12, 25),
    },
}


def is_holiday_simple(dt: datetime) -> bool:
    return dt.year in OFF_PEAK_DAYS and (dt.month, dt.day) in OFF_PEAK_DAYS[dt.year]
