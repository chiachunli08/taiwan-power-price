"""台電兩段式時間電價感測器."""
from datetime import datetime, time

from homeassistant.components.sensor import SensorEntity

from .holiday import is_holiday, is_summer

# 電價表 (元/度)
PRICE_TABLE = {
    "summer": {  # 夏月 (6/1-9/30)
        "weekday": {
            "peak": 5.16,
            "off_peak": 2.06,
        },
        "weekend": {
            "peak": 2.06,
            "off_peak": 2.06,
        },
    },
    "non_summer": {  # 非夏月
        "weekday": {
            "peak": 4.93,
            "off_peak": 1.99,
        },
        "weekend": {
            "peak": 1.99,
            "off_peak": 1.99,
        },
    },
}


class TaiwanPowerPriceSensor(SensorEntity):
    """台電電價感測器."""

    def __init__(self) -> None:
        self._attr_unique_id = "taiwan_power_price"
        self._attr_name = "台電當前電價"
        self._attr_native_unit_of_measurement = "元/度"
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> float:
        """取得當前電價."""
        return self._calculate_price()

    @property
    def extra_state_attributes(self) -> dict:
        """額外屬性."""
        now = datetime.now()
        is_summer_now = is_summer(now)
        is_holiday_now = is_holiday(now)
        is_weekend = now.weekday() >= 5
        
        price_type = self._get_price_type(now, is_summer_now, is_holiday_now, is_weekend)
        
        return {
            "is_summer": is_summer_now,
            "is_holiday": is_holiday_now,
            "is_weekend": is_weekend,
            "price_type": price_type,
            "period": "summer" if is_summer_now else "non_summer",
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _calculate_price(self) -> float:
        """計算當前電價."""
        now = datetime.now()
        is_summer_now = is_summer(now)
        is_holiday_now = is_holiday(now)
        is_weekend = now.weekday() >= 5 or is_holiday_now

        season = "summer" if is_summer_now else "non_summer"
        day_type = "weekend" if is_weekend else "weekday"
        price_type = self._get_price_type(now, is_summer_now, is_holiday_now, is_weekend)

        return PRICE_TABLE[season][day_type][price_type]

    def _get_price_type(self, now: datetime, is_summer: bool, is_holiday: bool, is_weekend: bool) -> str:
        """判斷當前是尖峰還是離峰."""
        if is_weekend or is_holiday:
            return "off_peak"

        current_time = now.time()

        if is_summer:
            if current_time >= time(9, 0):
                return "peak"
            return "off_peak"
        else:
            if (time(6, 0) <= current_time <= time(10, 59, 59)) or (current_time >= time(14, 0)):
                return "peak"
            return "off_peak"
