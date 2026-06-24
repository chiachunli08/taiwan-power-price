"""台電兩段式時間電價感測器."""
from datetime import datetime, time, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_point_in_time
import homeassistant.util.dt as dt_util

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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """設定感測器實體."""
    sensor = TaiwanPowerPriceSensor()
    async_add_entities([sensor], True)

    remove_scheduled_update = None

    @callback
    def _schedule_next_update(now: datetime) -> None:
        nonlocal remove_scheduled_update

        if remove_scheduled_update is not None:
            remove_scheduled_update()

        remove_scheduled_update = async_track_point_in_time(
            hass,
            _update,
            _get_next_update_time(now),
        )

    @callback
    def _update(now=None):
        sensor.async_schedule_update_ha_state(True)
        _schedule_next_update(dt_util.now())

    _schedule_next_update(dt_util.now())

    @callback
    def _remove_scheduled_update() -> None:
        if remove_scheduled_update is not None:
            remove_scheduled_update()

    entry.async_on_unload(_remove_scheduled_update)


class TaiwanPowerPriceSensor(SensorEntity):
    """台電電價感測器."""

    def __init__(self) -> None:
        self._attr_unique_id = "taiwan_power_price"
        self._attr_name = "台電當前電價"
        self._attr_native_unit_of_measurement = "TWD/kWh"
        self._attr_icon = "mdi:lightning-bolt"

    def update(self) -> None:
        """更新感測器狀態."""
        self._attr_native_value = _calculate_price(dt_util.now())

    @property
    def extra_state_attributes(self) -> dict:
        now = dt_util.now()
        return {
            "is_summer": is_summer(now),
            "is_holiday": is_holiday(now),
            "is_weekend": now.weekday() >= 5,
            "price_type": _get_price_type(now),
            "period": "summer" if is_summer(now) else "non_summer",
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        }


def _calculate_price(now) -> float:
    """計算電價."""
    is_summer_now = is_summer(now)
    is_holiday_now = is_holiday(now)
    is_weekend = now.weekday() >= 5 or is_holiday_now

    season = "summer" if is_summer_now else "non_summer"
    day_type = "weekend" if is_weekend else "weekday"
    price_type = _get_price_type(now)

    return PRICE_TABLE[season][day_type][price_type]


def _get_price_type(now) -> str:
    """判斷尖峰/離峰."""
    is_holiday_now = is_holiday(now)
    is_weekend = now.weekday() >= 5 or is_holiday_now
    
    if is_weekend or is_holiday_now:
        return "off_peak"

    current_time = now.time()
    is_summer_now = is_summer(now)

    if is_summer_now:
        return "peak" if current_time >= time(9, 0) else "off_peak"
    else:
        if (time(6, 0) <= current_time <= time(10, 59, 59)) or (current_time >= time(14, 0)):
            return "peak"
        return "off_peak"


def _get_next_update_time(now: datetime) -> datetime:
    """取得下一個電價或日期可能變更的時間點."""
    midnight = (now + timedelta(days=1)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    candidates = [midnight]

    if now.weekday() < 5 and not is_holiday(now):
        transition_times = [time(9, 0)] if is_summer(now) else [time(6, 0), time(11, 0), time(14, 0)]
        candidates.extend(
            now.replace(
                hour=transition_time.hour,
                minute=transition_time.minute,
                second=0,
                microsecond=0,
            )
            for transition_time in transition_times
        )

    return min(candidate for candidate in candidates if candidate > now)
