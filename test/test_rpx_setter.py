__author__ = 'ajb'

import sys

import os

roboplexx_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(roboplexx_parent_dir)

from roboplexx import rpx_util, rpx_prop
from roboplexx.devices import dev_basic
import rpx_proto

import unittest

@rpx_util.rpx_device
class TestDevice(dev_basic.RpxDevice):

    left_speed_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    left_speed_desc.propertyId = "left_speed"
    left_speed_desc.constraints.doubleTypeMaxVal = 100.0
    left_speed_desc.constraints.doubleTypeMinVal = -100.0

    right_speed_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    right_speed_desc.propertyId = "right_speed"
    right_speed_desc.constraints.doubleTypeMaxVal = 100.0
    right_speed_desc.constraints.doubleTypeMinVal = -100.0


    def __init__(self, device_id):
        dev_basic.RpxDevice.__init__(self, device_id)

    @rpx_util.getter(rpx_prop.string_prop_desc("demo_camera_version"))
    def get_demo_camera_version(self):
        return "Demo Camera 1.2.3"

    @rpx_util.getter(rpx_prop.string_prop_desc("video_url"))
    def get_demo_camera_video_url(self):
        return "http://theoldrobots.com/images6/rob268.JPG"

    @rpx_util.setter(rpx_prop.string_prop_desc("test_device_property"))
    def set_test_device_property(self, td_prop):
        self.test_device_property = td_prop

    @rpx_util.getter(rpx_prop.string_prop_desc("test_device_property"))
    def get_test_device_property(self):
        return self.test_device_property

    @rpx_util.setter(left_speed_desc, right_speed_desc)
    def set_motor_speeds(self, right_speed, left_speed):
        self.left_speed = left_speed
        self.right_speed = right_speed

    @rpx_util.getter(left_speed_desc)
    def get_left_speed(self):
        return self.left_speed

    @rpx_util.getter(right_speed_desc)
    def get_right_speed(self):
        return self.right_speed

    def drvr_init(self):
        pass

    def drvr_uninit(self):
        pass


class TestCase(unittest.TestCase):

    def test_setter_method(self):
        td = TestDevice("test_device")

        td.set_motor_speeds(right_speed=45, left_speed=22)
        self.assertEqual(22, td.left_speed)
        self.assertEqual(45, td.right_speed)

        td.set_test_device_property("abc")
        self.assertEqual("abc", td.test_device_property)


if __name__ == "__main__":
    unittest.main()
