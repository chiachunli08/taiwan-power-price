"""台電兩段式時間電價."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .sensor import TaiwanPowerPriceSensor

DOMAIN = "taiwan_power_price"


async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """設定整合."""
    async_add_entities([TaiwanPowerPriceSensor()])
    return True
