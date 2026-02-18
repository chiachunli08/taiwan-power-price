"""台電兩段式時間電價."""
from homeassistant.core import HomeAssistant


def setup(hass: HomeAssistant, config: dict) -> bool:
    """設定整合."""
    hass.helpers.discovery.load_platform("sensor", "taiwan_power_price", {}, config)
    return True
