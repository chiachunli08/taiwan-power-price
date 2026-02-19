"""台電兩段式時間電價."""
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.event as event

from .sensor import TaiwanPowerPriceSensor

DOMAIN = "taiwan_power_price"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """設定整合."""

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    async def update_state(now=None):
        """更新狀態."""
        from datetime import datetime
        from .sensor import _calculate_price

        current = datetime.now()
        price = _calculate_price(current)

        hass.states.async_set(
            "sensor.taiwan_power_price",
            price,
            {
                "unit_of_measurement": "元/度",
                "friendly_name": "台電當前電價",
                "icon": "mdi:lightning-bolt",
            }
        )

    update_state()

    event.async_track_time_interval(hass, update_state, interval=timedelta(minutes=1))

    return True
