"""台電兩段式時間電價感測器."""
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .sensor import TaiwanPowerPriceSensor

DOMAIN = "taiwan_power_price"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """從 UI 設定整合."""
    async_add_entities([TaiwanPowerPriceSensor()])
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool:
    """解除設定."""
    return True
