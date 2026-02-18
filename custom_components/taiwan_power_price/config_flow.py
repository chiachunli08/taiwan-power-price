"""台電兩段式時間電價設定流程."""
from homeassistant import config_entries


class TaiwanPowerPriceConfigFlow(config_entries.ConfigFlow, domain="taiwan_power_price"):
    """設定流程."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """使用者設定."""
        if user_input is not None:
            return self.async_create_entry(title="台電當前電價", data={})

        return self.async_show_form(step_id="user")
