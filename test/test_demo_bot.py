__author__ = 'ajb'

import sys

import os

roboplexx_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(roboplexx_parent_dir)

import roboplexx.rpx_host
import roboplexx.loadouts

import rpx_proto.rpx_pb2
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.demo_bot = roboplexx.loadouts.get_new_demo_bot()
        self.demo_bot.initialize_host()
        self.demo_bot.initialize_devices()

    def tearDown(self):
        for device in self.demo_bot.devices:
            device.deactivate()

        self.demo_bot = None
        self.bot_host = None

    def test_set_combo_drive_speeds_message(self):
        setSpeedMessage = rpx_proto.rpx_pb2.RpxMessage()
        setSpeedMessage.version = "1"

        firstOperation = setSpeedMessage.firstOperation
        firstOperation.delayBeforeStartInSec = 0.0
        firstOperation.blockUntilAllTasksComplete = True

        task = firstOperation.tasks.add()
        task.taskType = rpx_proto.rpx_pb2.Task.SetDevicePropertiesTaskType
        setSpeedTask = task.setDevicePropertiesTask
        setSpeedTask.hostId = "demobot"
        setSpeedTask.devicePath.append("diff_drive")

        left_speed = setSpeedTask.properties.add()
        left_speed.propertyId = "left_speed"
        left_speed.doubleVal = 51.5

        right_speed = setSpeedTask.properties.add()
        right_speed.propertyId = "right_speed"
        right_speed.doubleVal = 54.35

        msg = setSpeedMessage.SerializeToString()
        self.demo_bot.host.handle_message(msg)

        self.assertEqual(54.35, self.demo_bot.right_mc.motor_speed)
        self.assertEqual(51.5, self.demo_bot.left_mc.motor_speed)


    def test_bot_host_description(self):
        host_description = self.demo_bot.host.get_host_description()

        self.assertIsNotNone(host_description)
        self.assertEqual("demobot", host_description.hostId)
        self.assertEqual("demobot", host_description.hostLabel)

        self.assertEqual(4, len(host_description.deviceDescriptions))
        print "==="
        print host_description.deviceDescriptions[0].devicePropertyDescriptions[0]
        print ":::"




if __name__ == "__main__":
    unittest.main()
