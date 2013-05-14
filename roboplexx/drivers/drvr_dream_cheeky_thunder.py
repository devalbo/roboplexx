__author__ = 'ajb'

# a driver based on https://github.com/AlexNisnevich/sentinel

import sys

import os
import usb.core
from roboplexx.bot import rpx_util
from roboplexx.devices import dev_basic


# globals
FNULL = open(os.devnull, 'w')


@rpx_util.rpx_device
class DreamCheekyThunder(dev_basic.RpxDevice):
    # Low level launcher driver commands
    # this code mostly taken from https://github.com/nmilford/stormLauncher
    # with bits from https://github.com/codedance/Retaliation
    def __init__(self):
        self.usb_conn = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.usb_conn is None:
            raise ValueError('Missile launcher not found.')
        if sys.platform == 'linux2' and self.usb_conn.is_kernel_driver_active(0) is True:
            self.usb_conn.detach_kernel_driver(0)
        self.usb_conn.set_configuration()

    @rpx_util.command("turret_up")
    def turretUp(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("turret_down")
    def turretDown(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("turret_left")
    def turretLeft(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("turret_right")
    def turretRight(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("turret_stop")
    def turretStop(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("fire")
    def turretFire(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("light_on")
    def ledOn(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @rpx_util.command("light_off")
    def ledOff(self):
        self.usb_conn.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

