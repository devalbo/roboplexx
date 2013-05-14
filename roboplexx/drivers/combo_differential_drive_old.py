from roboplexx.bot import rpx_util
from roboplexx.devices import dev_basic
import rpx_proto

@rpx_util.rpx_device
class DifferentialDrive(dev_basic.RpxDevice):

    percentage_double_constraints = rpx_proto.descriptions_pb2.PropertyTypeConstraints()
    percentage_double_constraints.doubleTypeMaxVal = 100.0
    percentage_double_constraints.doubleTypeMinVal = -100.0

    motor_speeds_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    motor_speeds_desc.propertyId = "motor_speeds"
    motor_speeds_desc.type = rpx_proto.descriptions_pb2.SubPropertiesType

    left_speed_desc = motor_speeds_desc.subPropertyDescriptions.add()
    left_speed_desc.propertyId = "left_speed"
    pc = left_speed_desc.constraints
    pc.doubleTypeMaxVal = 100.0
    pc.doubleTypeMinVal = -100.0

    right_speed_desc = motor_speeds_desc.subPropertyDescriptions.add()
    right_speed_desc.propertyId = "right_speed"
    pc = right_speed_desc.constraints
    pc.doubleTypeMaxVal = 100.0
    pc.doubleTypeMinVal = -100.0

    def __init__(self, device_id, motor_left, motor_right):
        dev_basic.RpxDevice.__init__(self, device_id)
        self._motor_left = motor_left
        self._motor_right = motor_right

    # @rpx_util.rpx_multi_getter("motor_speeds")
    # def get_motor_speeds(self):
    #   return {"left_speed": self._motor_left.get_motor_speed(),
    #           "right_speed": self._motor_right.get_motor_speed()}

    # @rpx_util.rpx_multi_setter("motor_speeds", ["left_speed", "right_speed"])
    # def set_motor_speeds(self, left_speed, right_speed):
    #   print "SETTING MOTOR SPEEDS"
    #   self._motor_left.set_motor_speed(left_speed)
    #   self._motor_right.set_motor_speed(right_speed)
    #   return {"left_speed": self._motor_left.get_motor_speed(),
    #           "right_speed": self._motor_right.get_motor_speed()}

    @rpx_util.setter(motor_speeds_desc)
    def set_motor_speeds(self, motor_speeds):
        print "SETTING MOTOR SPEEDS", motor_speeds
        ms_dict = rpx_util.property_to_py(motor_speeds)
        # print ms_dict
        # left_speed = rpx_util.get_subproperty(motor_speeds, "left_speed")
        # right_speed = rpx_util.get_subproperty(motor_speeds, "right_speed")
        left_speed = ms_dict["left_speed"]
        right_speed = ms_dict["right_speed"]
        print "left_speed %s" % left_speed
        print "right_speed %s" % right_speed
        self._motor_left.set_motor_speed(left_speed)
        self._motor_right.set_motor_speed(right_speed)
        # return {"left_speed": self._motor_left.get_motor_speed(),
        #         "right_speed": self._motor_right.get_motor_speed()}
        return self.get_motor_speeds()

    @rpx_util.getter(motor_speeds_desc)
    def get_motor_speeds(self):
          # return {"left_speed": self._motor_left.get_motor_speed(),
          #         "right_speed": self._motor_right.get_motor_speed()}
        motor_speeds = rpx_proto.common_pb2.Property()
        motor_speeds.type = rpx_proto.common_pb2.SubPropertiesType
        motor_speeds.propertyId = "motor_speeds"

        rpx_util.add_double_property(motor_speeds, "left_speed", self._motor_left.get_motor_speed())
        rpx_util.add_double_property(motor_speeds, "right_speed", self._motor_right.get_motor_speed())
        return motor_speeds


    def drvr_init(self):
        pass

    def drvr_un_init(self):
        pass

