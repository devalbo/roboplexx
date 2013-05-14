import os
from roboplexx import basebot, drivers, rpx_util

_IDENTIFIER_REGEX = "[a-zA-Z_0-9]*"


def get_loadout_files_dir():
    return os.path.join(os.path.dirname(os.path.realpath(rpx_util.__file__)),
                        "loadout_configs")


def get_new_demo_bot():
    demobot_prop_file = os.path.join(get_loadout_files_dir(),
                                     "demobot.properties")
    return load_from_property_file(demobot_prop_file)


def load_from_property_file(filename):
    import jprops, re
    with open(filename) as fp:
        properties = jprops.load_properties(fp)

        # figure out host info from properties
        host_driver = properties["bot.host"]
        host_id = properties.get("bot.host.id", "")
        rpx_password = properties.get("bot.host.rpx_password", "")

        bot = basebot.BaseBot()
        bot.host = getattr(drivers, host_driver)(host_id, rpx_password)
        bot.host.properties_file = filename

        bot.devices = []

        # find/apply host properties for each device
        host_rpx_prop_regex = re.compile("bot\.host\.props\.(%s)" % _IDENTIFIER_REGEX)
        host_rpx_prop_ids_and_values = [(match.group(1), properties[p])
                                        for p in properties
                                        for match in [host_rpx_prop_regex.search(p)]
                                        if match]
        for rpx_prop_id, rpx_prop_value in host_rpx_prop_ids_and_values:
            rpx_util.apply_rpx_property_string_value_to_device(bot.host, rpx_prop_id, rpx_prop_value)

        # figure out devices/device_ids from properties
        device_id_prop_regex = re.compile("bot.devices.(%s)$" % _IDENTIFIER_REGEX)
        device_ids_and_drivers = [(match.group(1), properties[p])
                                  for p in properties
                                  for match in [device_id_prop_regex.search(p)]
                                  if match]

        # create devices; find/apply RPX properties for each device
        for device_id, device_driver in device_ids_and_drivers:
            device = getattr(drivers, device_driver)(device_id)
            setattr(bot, device_id, device)
            device_rpx_prop_regex = re.compile("bot\.devices\.%s\.props\.(%s)" % (device_id, _IDENTIFIER_REGEX))
            device_rpx_prop_ids_and_values = [(match.group(1), properties[p])
                                              for p in properties
                                              for match in [device_rpx_prop_regex.search(p)]
                                              if match]
            for rpx_prop_id, rpx_prop_value in device_rpx_prop_ids_and_values:
                rpx_util.apply_rpx_property_string_value_to_device(device, rpx_prop_id, rpx_prop_value)

            bot.devices.append(device)

        # find/attach subdevices to devices
        for device_id, device_driver in device_ids_and_drivers:
            subdevice_regex = re.compile("bot.devices.%s.subdevices.(%s)" % (device_id, _IDENTIFIER_REGEX))
            subdevice_sub_ids_and_bot_ids = [(match.group(1), properties[p])
                                             for p in properties
                                             for match in [subdevice_regex.search(p)]
                                             if match]

            device = getattr(bot, device_id)
            for sub_id, bot_id in subdevice_sub_ids_and_bot_ids:
                sub_id_on_bot = bot_id.split("bot.devices.", 1)[1]
                sub_device = getattr(bot, sub_id_on_bot)
                setattr(device, sub_id, sub_device)

        return bot


def save_to_property_file(bot, filename):
    import jprops

    with open(filename, "w") as f:
        bot_props = {"bot.host": bot.host.__class__.__name__,
                     "bot.host.id": bot.host.host_id,
                     "bot.host.password": bot.host.rpx_password,
                     "bot.host.props.roboplexx_id": str(bot.host.roboplexx_id),
                     "bot.host.props.debug_mode_on": str(bot.host.debug_mode_on),
                     "bot.host.props.web_app_enabled": str(bot.host.web_app_enabled),
                     "bot.host.props.web_app_host_name": str(bot.host.web_app_host_name),
                     "bot.host.props.web_app_port": str(bot.host.web_app_port),
                     }

        for device in bot.devices:
            bot_props["bot.devices.%s" % device.device_id] = device.__class__.__name__
            persist_props = device.__rpx_prop_info__
            for prop_name, (prop_desc, get_method_name, set_method_name) in persist_props.iteritems():
                getter = getattr(device, get_method_name)
                value = getter()
                if prop_desc.persist:
                    bot_props["bot.devices.%s.props.%s" % (device.device_id, prop_name)] = str(value)

            if hasattr(device, "sub_devices"):
                for sub_device_id, sub_device in device.sub_devices.iteritems():
                    bot_props["bot.devices.%s.subdevices.%s" % (device.device_id, sub_device_id)] = \
                        "bot.devices.%s" % sub_device.device_id

        jprops.store_properties(f, bot_props)