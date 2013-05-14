from roboplexx import rpx_util, devices, rpx_prop

__author__ = 'ajb'


# @rpx_util.rpx_device
class DemoMultiMotorController(devices.MultiHost):

    def __init__(self, device_id):
        devices.MultiHost.__init__(self, device_id)
        self._initialized = False

    # @rpx_util.rpx_getter("demo_multimotor_version")
    @rpx_util.getter(rpx_prop.string_prop_desc("demo_multimotor_version"))
    def get_demo_motor_version(self):
        return "Demo MultiMotor 1.2.3"

    def drvr_init(self):
        self._initialized = True

    def drvr_un_init(self):
        self._initialized = False

    def get_subdevices(self):
        if not self._initialized:
          raise rpx_util.RpxDevNotInitializedError()
        self._mc1 = MotorPoint("mc1")
        self._mc2 = MotorPoint("mc2")
        self._mc3 = MotorPoint("mc3")
        self._mc4 = MotorPoint("mc4")
        return (self._mc1, self._mc2, self._mc3, self._mc4)


class MotorPoint(devices.McBasic):

    def __init__(self, device_id):
        devices.McBasic.__init__(self, device_id)
        self._motor_speed = "0"

    def drvr_init(self):
        pass

    def drvr_un_init(self):
        pass

    def drvr_set_motor_speed(self, speed):
        self._motor_speed = speed
        return self._motor_speed

    def drvr_get_motor_speed(self):
        return self._motor_speed