"""台電兩段式時間電價感測器."""
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})


def setup_platform(hass: HomeAssistant, config: dict, add_entities: AddEntitiesCallback, discovery_info=None):
    """傳統方式設定感測器."""
    add_entities([TaiwanPowerPriceSensor()])


class TaiwanPowerPriceSensor(SensorEntity):
    """台電電價感測器."""

    def __init__(self) -> None:
        self._attr_unique_id = "taiwan_power_price"
        self._attr_name = "台電當前電價"
        self._attr_native_unit_of_measurement = "元/度"
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> float:
        from datetime import datetime
        return self._calculate_price(datetime.now())

    @property
    def extra_state_attributes(self) -> dict:
        from datetime import datetime
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

    def _calculate_price(self, now) -> float:
        is_summer_now = is_summer(now)
        is_holiday_now = is_holiday(now)
        is_weekend = now.weekday() >= 5 or is_holiday_now

        season = "summer" if is_summer_now else "non_summer"
        day_type = "weekend" if is_weekend else "weekday"
        price_type = self._get_price_type(now, is_summer_now, is_holiday_now, is_weekend)

        return PRICE_TABLE[season][day_type][price_type]

    def _get_price_type(self, now, is_summer: bool, is_holiday: bool, is_weekend: bool) -> str:
        from datetime import time
        if is_weekend or is_holiday:
            return "off_peak"

        current_time = now.time()

        if is_summer:
            return "peak" if current_time >= time(9, 0) else "off_peak"
        else:
            if (time(6, 0) <= current_time <= time(10, 59, 59)) or (current_time >= time(14, 0)):
                return "peak"
            return "off_peak"
