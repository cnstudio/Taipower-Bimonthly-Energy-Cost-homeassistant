"""Config flow for TaiPower Energy Cost integration."""
import logging
from datetime import datetime
import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import selector

from .const import (
    CONFIG_FLOW_VERSION,
    CONF_BIMONTHLY_ENERGY,
    CONF_METER_START_DAY,
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate that the user input allows us to connect to DataPoint.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    states_source = hass.states.get(data[CONF_BIMONTHLY_ENERGY])
    if states_source is None:
        raise EntityNotExist
    return True


class TaiPowerCostFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TaiPower Energy Cost integration."""

    VERSION = CONFIG_FLOW_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return TaiPowerCostOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            taipower_energy_cost = "taipower_energy_cost"
            await self.async_set_unique_id(
                    f"{taipower_energy_cost}-{user_input[CONF_BIMONTHLY_ENERGY]}"
                )
            self._abort_if_unique_id_configured()

            ret = False
            try:
                ret = await validate_input(self.hass, user_input)
            except EntityNotExist:
                errors["base"] = "entitynotexist"
            except ValueError:
                errors["base"] = "dataformaterror"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if ret:
                title = "TaiPower Energy Cost"
                return self.async_create_entry(
                    title=title, data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_BIMONTHLY_ENERGY): selector.selector(
                    {"entity": {"domain": "sensor"}},
                ),
                # pylint: disable=unnecessary-lambda
                vol.Required(
                    CONF_METER_START_DAY,
                    default=lambda: datetime.now().strftime("%Y-%m-%d")): selector.selector(
                        {"date": {}},
                    )
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


class TaiPowerCostOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            errors = {}
            ret = False
            try:
                ret = await validate_input(self.hass, user_input)
            except EntityNotExist:
                errors["base"] = "entitynotexist"
            except ValueError:
                errors["base"] = "dataformaterror"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            if ret:
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_options_schema(),
        )

    def _get_options_schema(self):
        return vol.Schema(
            {
                vol.Required(
                    CONF_BIMONTHLY_ENERGY,
                    default=_get_config_value(
                        self.config_entry, CONF_BIMONTHLY_ENERGY, "")
                ): selector.selector(
                    {"entity": {"domain": "sensor"}},
                ),
                vol.Required(
                    CONF_METER_START_DAY): selector.selector({"date": {}}),
            }
        )


def _get_config_value(config_entry, key, default):
    if config_entry.options:
        return config_entry.options.get(key, default)
    return config_entry.data.get(key, default)


class EntityNotExist(exceptions.HomeAssistantError):
    """Error to indicate Entity not exist."""
