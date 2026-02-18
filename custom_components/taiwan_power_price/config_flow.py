"""台電兩段式時間電價設定流程."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback


class TaiwanPowerPriceConfigFlow(config_entries.ConfigFlow, domain="taiwan_power_price"):
    """設定流程."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """使用者設定."""
        if user_input is not None:
            return self.async_create_entry(title="台電兩段式時間電價", data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """取得選項流程."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """選項流程."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """初始化選項."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init")
