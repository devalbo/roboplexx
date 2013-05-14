from roboplexx.bot import loadouts, rpx_host, drivers
from roboplexx.connect import rpx_connect
# from roboplexx.www import rpx_app_host

__author__ = 'ajb'

import os
import sys
roboplexx_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(roboplexx_parent_dir)


demo_bot = loadouts.DemoBot()
demo_bot.host_id = "demobot"
demo_bot.host = drivers.RpxHostDriver(demo_bot.host_id)

for device in demo_bot.devices:
    device.activate()
    demo_bot.host.register_device(device)

app_host = rpx_app_host.LocalAppHost()

connection = rpx_connect.connect_bot_to_app(bot_host, app_host)


# start application
if __name__ == "__main__":
    print "Started"