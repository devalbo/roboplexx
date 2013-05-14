__author__ = 'ajb'

import roboplexx

web_app_host = "http://localhost:5000"

bot_properties_file = "demobot.properties"

demo_bot = roboplexx.loadouts.load_from_property_file(bot_properties_file)
demo_bot.initialize_host()
demo_bot.initialize_devices()

from time import sleep
sleep(2)

if not demo_bot.host.host_id:
    register_response = demo_bot.register_with_web_app(web_app_host)
    response_json = register_response.json()

    print response_json
    new_host_id = response_json["host_id"]
    rpx_pwd = response_json["host_password"]
    demo_bot.host.device_id = new_host_id
    print "RPX PWD: '%s' <<< " % demo_bot.host.rpx_password
    demo_bot.host.rpx_password = rpx_pwd

    roboplexx.loadouts.save_to_property_file(demo_bot, bot_properties_file)

    print register_response

checkin_response = demo_bot.checkin_with_web_app(web_app_host)
checkin_response = checkin_response.json()
print checkin_response

demo_bot.listen_command_queue(checkin_response["command_queue_url"])