"""台電兩段式時間電價."""
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.event as event

DOMAIN = "taiwan_power_price"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """設定整合."""
    
    entity_id = "sensor.taiwan_power_price"
    
    @callback
    def update_state(now=None):
        """更新狀態."""
        from datetime import datetime
        from .sensor import _calculate_price
        
        current = datetime.now()
        price = _calculate_price(current)
        
        hass.states.async_set(
            entity_id,
            price,
            {
                "unit_of_measurement": "元/度",
                "friendly_name": "台電當前電價",
                "icon": "mdi:lightning-bolt",
            }
        )
    
    # 初始設定
    update_state()
    
    # 定時更新（每分鐘）
    event.async_track_time_interval(hass, update_state, interval=timedelta(minutes=1))
    
    return True
