from roboplexx import rpx_util, devices, rpx_prop

@rpx_util.rpx_device
class DemoMotorController(devices.McBasic):

    def __init__(self, device_id):
        devices.McBasic.__init__(self, device_id)
        self._connection_string = ""
        self._motor_speed = "0"

    @rpx_util.getter(rpx_prop.string_prop_desc("demo_motor_version"))
    def get_demo_motor_version(self):
        return "Demo Motor 1.2.3"

    def drvr_init(self):
        print "In drvr_init"
        pass

    def drvr_uninit(self):
        pass

    def drvr_set_motor_speed(self, speed):
        self._motor_speed = speed
        print "Setting demo motor speed [%s] >> %s" % (self.device_id, speed)
        return self._motor_speed

    def drvr_get_motor_speed(self):
        return self._motor_speed
