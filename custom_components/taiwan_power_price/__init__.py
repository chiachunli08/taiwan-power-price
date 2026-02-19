"""台電兩段式時間電價."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "taiwan_power_price"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """設定整合."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """移除整合."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
