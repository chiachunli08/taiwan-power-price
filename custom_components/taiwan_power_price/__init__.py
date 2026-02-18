"""台電兩段式時間電價感測器."""
import asyncio

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .sensor import TaiwanPowerPriceSensor

__all__ = ["TaiwanPowerPriceSensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """設定整合（手動設定方式）."""
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            "taiwan_power_price", context={"source": config_entries.SOURCE_IMPORT}
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool:
    """從 UI/整合設定."""
    hass.async_add_entities([TaiwanPowerPriceSensor()])
    return True
