"""台電兩段式時間電價."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "taiwan_power_price"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """設定整合."""
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    
    # 延遲載入，避免循環依賴
    async def add_entities():
        from .sensor import TaiwanPowerPriceSensor
        hass.async_add_entities([TaiwanPowerPriceSensor()])
    
    # 等待事件循環準備好
    hass.async_create_task(add_entities())
    return True
