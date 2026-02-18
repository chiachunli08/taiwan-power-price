"""台電離峰日與夏月判斷."""
from datetime import date, datetime
from typing import Tuple

try:
    from lunardate import LunarDate
    HAS_LUNAR = True
except ImportError:
    HAS_LUNAR = False


def is_summer(dt: datetime) -> bool:
    """判斷是否為夏月 (6/1-9/30)."""
    return 6 <= dt.month <= 9


def is_holiday(dt: datetime) -> bool:
    """判斷是否為台電指定離峰日."""
    # 先檢查預定義清單（2024-2030）
    if is_holiday_simple(dt):
        return True
    
    # 轉換為農曆（如果可用）
    lunar_date = None
    if HAS_LUNAR:
        try:
            lunar_date = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)
        except Exception:
            pass

    # 國定假日 (陽曆)
    if _is_western_holiday(dt):
        return True

    # 農曆假日
    if lunar_date and _is_lunar_holiday(lunar_date):
        return True

    return False


def _is_western_holiday(dt: datetime) -> bool:
    """判斷陽曆國定假日."""
    # 元旦
    if dt.month == 1 and dt.day == 1:
        return True
    
    # 和平紀念日 (2/28)
    if dt.month == 2 and dt.day == 28:
        return True
    
    # 兒童節 (4/4)
    if dt.month == 4 and dt.day == 4:
        return True
    
    # 清明節 (4/4 或 4/5) - 採用節氣計算，這裡簡化為 4/5
    if dt.month == 4 and dt.day == 5:
        return True
    
    # 勞動節 (5/1)
    if dt.month == 5 and dt.day == 1:
        return True
    
    # 端午節 (農曆五月五日) - 需農曆判斷，這裡用簡化版
    # 中秋節 (農曆八月十五日) - 需農曆判斷
    
    # 國慶日 (10/10)
    if dt.month == 10 and dt.day == 10:
        return True
    
    return False


def _is_lunar_holiday(lunar_date) -> bool:
    """判斷農曆假日."""
    if not lunar_date:
        return False
    
    month = lunar_date.month
    day = lunar_date.day

    # 春節: 農曆正月初一至初五 (除夕也已包含)
    # 春節假期通常是除夕到初五
    if month == 1 and 1 <= day <= 5:
        return True
    
    # 端午節: 農曆五月五日
    if month == 5 and day == 5:
        return True
    
    # 中秋節: 農曆八月十五日
    if month == 8 and day == 15:
        return True

    return False


def is_lunar_new_year_eve(dt: datetime) -> bool:
    """判斷是否為農曆除夕."""
    if not HAS_LUNAR:
        return False
    
    try:
        lunar_date = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)
        # 除夕是農曆12月最後一天
        return lunar_date.month == 12 and lunar_date.isLeapMonth == False
    except Exception:
        return False


# 預定義的離峰日清單 (2024-2030)
# 格式: (月, 日)
OFF_PEAK_DAYS = {
    # 2024
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2024: 2/9(除夕) ~ 2/14
    (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14),
    # 端午節 2024: 6/10
    (6, 10),
    # 中秋節 2024: 9/17
    (9, 17),
    
    # 2025
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2025: 1/28(除夕) ~ 2/1
    (1, 28), (1, 29), (1, 30), (1, 31), (2, 1),
    # 端午節 2025: 5/31
    (5, 31),
    # 中秋節 2025: 10/6
    (10, 6),
    
    # 2026
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2026: 2/16(除夕) ~ 2/20
    (2, 16), (2, 17), (2, 18), (2, 19), (2, 20),
    # 端午節 2026: 6/19
    (6, 19),
    # 中秋節 2026: 9/25
    (9, 25),
    
    # 2027
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2027: 2/6(除夕) ~ 2/10
    (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
    # 端午節 2027: 6/9
    (6, 9),
    # 中秋節 2027: 9/15
    (9, 15),
    
    # 2028
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2028: 1/26(除夕) ~ 1/30
    (1, 26), (1, 27), (1, 28), (1, 29), (1, 30),
    # 端午節 2028: 5/28
    (5, 28),
    # 中秋節 2028: 10/3
    (10, 3),
    
    # 2029
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2029: 2/13(除夕) ~ 2/17
    (2, 13), (2, 14), (2, 15), (2, 16), (2, 17),
    # 端午節 2029: 6/16
    (6, 16),
    # 中秋節 2029: 9/22
    (9, 22),
    
    # 2030
    (1, 1),    # 元旦
    (2, 28),   # 和平紀念日
    (4, 4),    # 兒童節
    (4, 5),    # 清明節
    (5, 1),    # 勞動節
    (10, 10),  # 國慶日
    # 春節 2030: 2/3(除夕) ~ 2/7
    (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
    # 端午節 2030: 6/5
    (6, 5),
    # 中秋節 2030: 9/12
    (9, 12),
}


def is_holiday_simple(dt: datetime) -> bool:
    """簡化的假日判斷（使用預定義清單）."""
    return (dt.month, dt.day) in OFF_PEAK_DAYS
