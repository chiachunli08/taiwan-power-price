"""台電兩段式時間電價感測器."""
from datetime import datetime, time
import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .holiday import is_holiday, is_summer

_LOGGER = logging.getLogger(__name__)

# 電價表 (元/度)
PRICE_TABLE = {
    "summer": {  # 夏月 (6/1-9/30)
        "weekday": {
            "peak": 5.16,      # 週一至週五 尖峰 09:00-24:00
            "off_peak": 2.06,  # 週一至週五 離峰 00:00-09:00
        },
        "weekend": {
            "peak": 2.06,      # 週六日及離峰日 全日
            "off_peak": 2.06,
        },
    },
    "non_summer": {  # 非夏月
        "weekday": {
            "peak": 4.93,      # 週一至週五 尖峰 06:00-11:00, 14:00-24:00
            "off_peak": 1.99,  # 週一至週五 離峰 00:00-06:00, 11:00-14:00
        },
        "weekend": {
            "peak": 1.99,      # 週六日及離峰日 全日
            "off_peak": 1.99,
        },
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """設定整合."""
    sensor = TaiwanPowerPriceSensor()
    async_add_entities([sensor])


class TaiwanPowerPriceSensor(SensorEntity):
    """台電電價感測器."""

    _attr_unique_id = "taiwan_power_price"
    _attr_name = "台電當前電價"
    _attr_native_unit_of_measurement = "元/度"
    _attr_icon = "mdi:lightning-bolt"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self) -> None:
        self._attr_native_value = 0.0

    def update(self) -> None:
        """更新資料."""
        self._attr_native_value = self._calculate_price()
        self._attr_extra_state_attributes = self._get_attributes()

    async def async_update(self) -> None:
        """非同步更新資料."""
        self._attr_native_value = self._calculate_price()
        self._attr_extra_state_attributes = self._get_attributes()

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
            else:
                return "off_peak"
        else:
            if (time(6, 0) <= current_time <= time(10, 59, 59)) or (current_time >= time(14, 0)):
                return "peak"
            else:
                return "off_peak"

    def _get_attributes(self) -> dict:
        """取得屬性."""
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
