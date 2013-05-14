from roboplexx import rpx_util
from roboplexx.devices import dev_basic
import rpx_proto

@rpx_util.rpx_device
class DifferentialDrive(dev_basic.RpxDevice):

    left_speed_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    left_speed_desc.propertyId = "left_speed"
    left_speed_desc.propertyLabel = "left_speed"
    left_speed_desc.propertyType = rpx_proto.descriptions_pb2.DoubleType
    left_speed_desc.constraints.doubleTypeMinVal = -100.0
    left_speed_desc.constraints.doubleTypeMaxVal = 100.0

    right_speed_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    right_speed_desc.propertyId = "right_speed"
    right_speed_desc.propertyLabel = "right_speed"
    right_speed_desc.propertyType = rpx_proto.descriptions_pb2.DoubleType
    right_speed_desc.constraints.doubleTypeMinVal = -100.0
    right_speed_desc.constraints.doubleTypeMaxVal = 100.0

    sub_device_ids = ["left_mc", "right_mc"]


    def __init__(self, device_id):
        dev_basic.RpxDevice.__init__(self, device_id)
        self._sub_devices = {}
        for sub_device_id in self.sub_device_ids:
            self._sub_devices[sub_device_id] = None


    @property
    def left_mc(self):
        return self._sub_devices["left_mc"]

    @left_mc.setter
    def left_mc(self, value):
        self._sub_devices["left_mc"] = value


    @property
    def right_mc(self):
        return self._sub_devices["right_mc"]

    @right_mc.setter
    def right_mc(self, value):
        self._sub_devices["right_mc"] = value

    @property
    def sub_devices(self):
        return self._sub_devices

    # @rpx_util.setter(left_speed_desc, right_speed_desc)
    # def set_motor_speeds(self, left_speed=None, right_speed=None):
    #
    #     if left_speed is not None:
    #         self.left_mc.motor_speed = left_speed
    #
    #     if right_speed is not None:
    #         self.right_mc.motor_speed = right_speed
    #
    #     return self.get_motor_speeds()


    @rpx_util.getter(left_speed_desc)
    def get_left_speed(self):
        return self.left_mc.get_motor_speed()

    @rpx_util.getter(right_speed_desc)
    def get_right_speed(self):
        return self.right_mc.get_motor_speed()

    @rpx_util.setter(left_speed_desc)
    def set_left_speed(self, value):
        return self.left_mc.set_motor_speed(value)


    @rpx_util.setter(right_speed_desc)
    def set_right_speed(self, value):
        return self.right_mc.set_motor_speed(value)


    # @rpx_util.getter(left_speed_desc, right_speed_desc)
    def get_motor_speeds(self):
          # return {"left_speed": self._motor_left.get_motor_speed(),
          #         "right_speed": self._motor_right.get_motor_speed()}
        motor_speeds = rpx_proto.common_pb2.Property()
        # motor_speeds.propertyType = rpx_proto.descriptions_pb2.SubPropertiesType
        motor_speeds.propertyId = "motor_speeds"

        # rpx_util.add_double_property(motor_speeds, "left_speed", self._motor_left.get_motor_speed())
        # rpx_util.add_double_property(motor_speeds, "right_speed", self._motor_right.get_motor_speed())
        return motor_speeds

    @rpx_util.command("stop")
    def stop(self):
        print "Stop"


    def drvr_init(self):
        pass

    def drvr_uninit(self):
        pass

