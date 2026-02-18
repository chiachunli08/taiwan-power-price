"""台電兩段式時間電價感測器."""
from datetime import datetime, time

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
import voluptuous as vol

from .holiday import is_holiday, is_summer

# 電價表 (元/度)
PRICE_TABLE = {
    "summer": {
        "weekday": {"peak": 5.16, "off_peak": 2.06},
        "weekend": {"peak": 2.06, "off_peak": 2.06},
    },
    "non_summer": {
        "weekday": {"peak": 4.93, "off_peak": 1.99},
        "weekend": {"peak": 1.99, "off_peak": 1.99},
    },
}


def setup(hass: HomeAssistant, config: dict) -> bool:
    """設定感測器."""
    hass.states.set("sensor.taiwan_power_price", 0, {
        "unit_of_measurement": "元/度",
        "friendly_name": "台電當前電價",
        "icon": "mdi:lightning-bolt",
    })
    
    def update_price():
        """更新電價."""
        now = datetime.now()
        price = _calculate_price(now)
        is_summer_now = is_summer(now)
        is_holiday_now = is_holiday(now)
        is_weekend = now.weekday() >= 5
        price_type = _get_price_type(now, is_summer_now, is_holiday_now, is_weekend)
        
        hass.states.set("sensor.taiwan_power_price", price, {
            "unit_of_measurement": "元/度",
            "friendly_name": "台電當前電價",
            "icon": "mdi:lightning-bolt",
            "is_summer": is_summer_now,
            "is_holiday": is_holiday_now,
            "is_weekend": is_weekend,
            "price_type": price_type,
            "period": "summer" if is_summer_now else "non_summer",
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        })
    
    # 定時更新
    import homeassistant.helpers.event as event
    event.track_time_interval(hass, update_price, interval=60)
    
    # 初始更新
    update_price()
    
    return True


def _calculate_price(now) -> float:
    """計算電價."""
    is_summer_now = is_summer(now)
    is_holiday_now = is_holiday(now)
    is_weekend = now.weekday() >= 5 or is_holiday_now

    season = "summer" if is_summer_now else "non_summer"
    day_type = "weekend" if is_weekend else "weekday"
    price_type = _get_price_type(now, is_summer_now, is_holiday_now, is_weekend)

    return PRICE_TABLE[season][day_type][price_type]


def _get_price_type(now, is_summer: bool, is_holiday: bool, is_weekend: bool) -> str:
    """判斷尖峰/離峰."""
    if is_weekend or is_holiday:
        return "off_peak"

    current_time = now.time()

    if is_summer:
        return "peak" if current_time >= time(9, 0) else "off_peak"
    else:
        if (time(6, 0) <= current_time <= time(10, 59, 59)) or (current_time >= time(14, 0)):
            return "peak"
        return "off_peak"
