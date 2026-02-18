"""台電兩段式時間電價."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .sensor import TaiwanPowerPriceSensor

DOMAIN = "taiwan_power_price"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """設定整合."""
    hass.async_add_entities([TaiwanPowerPriceSensor()])
    return True
