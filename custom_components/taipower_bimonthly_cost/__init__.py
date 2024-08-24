"""TheTaiPower Energy Cost integration."""
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BIMONTHLY_ENERGY,
    DOMAIN,
    PLATFORMS
)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up a TaiPower Bimonthly Energy Cost entry."""

    # migrate data (also after first setup) to options
    if config_entry.data:
        hass.config_entries.async_update_entry(config_entry, data={},
                                               options=config_entry.data)

    data = hass.data.setdefault(DOMAIN, {})
    data[config_entry.entry_id] = {
        CONF_BIMONTHLY_ENERGY: _get_config_value(config_entry, CONF_BIMONTHLY_ENERGY, "")
    }
    for platform in PLATFORMS:
        hass.async_create_task(
            await hass.config_entries.async_forward_entry_setups(config_entry, platform)
        )

    return True


async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    return unload_ok


def _get_config_value(config_entry, key, default):
    if config_entry.options:
        return config_entry.options.get(key, default)
    return config_entry.data.get(key, default)
