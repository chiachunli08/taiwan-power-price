"""台電兩段式時間電價感測器."""
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .sensor import TaiwanPowerPriceSensor

DOMAIN = "taiwan_power_price"


async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool:
    """從 UI 設定整合."""
    sensor = TaiwanPowerPriceSensor()
    hass.async_add_entities([sensor])
    return True
