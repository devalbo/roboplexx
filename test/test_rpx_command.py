__author__ = 'ajb'

import sys

import os

roboplexx_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(roboplexx_parent_dir)

from roboplexx import rpx_util, rpx_prop
from roboplexx.devices import dev_basic
from roboplexx.drivers.drvr_host import RpxHostDriver
import rpx_proto

import unittest

@rpx_util.rpx_device
class TestDevice(dev_basic.RpxDevice):


    def __init__(self, device_id):
        dev_basic.RpxDevice.__init__(self, device_id)
        self.command_received = False

    @rpx_util.command("command_under_test")
    def command_under_test(self):
        self.command_received = True

    def drvr_init(self):
        pass

    def drvr_uninit(self):
        pass


class TestCase(unittest.TestCase):

    def test_setter_method(self):
        td = TestDevice("test_device")
        self.assertFalse(td.command_received)

        host = RpxHostDriver("test_host", "test_password")
        host.register_device(td)

        cmdMessage = rpx_proto.rpx_pb2.RpxMessage()
        cmdMessage.version = "1"

        firstOperation = cmdMessage.firstOperation
        firstOperation.delayBeforeStartInSec = 0.0
        firstOperation.blockUntilAllTasksComplete = True

        cmdTask = firstOperation.tasks.add()

        cmdTask.taskType = rpx_proto.rpx_pb2.Task.DoDeviceCommandsTaskType
        cmdTask = cmdTask.doDeviceCommandsTask
        cmdTask.hostId = "test_host"
        cmdTask.devicePath.append("test_device")
        cmdTask.commandId = "command_under_test"

        msg = cmdMessage.SerializeToString()
        host.handle_message(msg)
        self.assertTrue(td.command_received)


if __name__ == "__main__":
    unittest.main()
