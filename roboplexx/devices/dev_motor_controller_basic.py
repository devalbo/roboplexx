from roboplexx import rpx_util, rpx_prop
from roboplexx.devices import dev_basic

__author__ = 'ajb'

@rpx_util.rpx_device
class McBasic(dev_basic.RpxDevice):

    direction_flipped_description = rpx_prop.boolean_property_description("direction_flipped")
    direction_flipped_description.persist = True
    connection_string_description = rpx_prop.string_prop_desc("connection_string")
    connection_string_description.persist = True
    motor_speed_description = rpx_prop.ranged_double_property_description("motor_speed", -100.0, 100.0)

    def __init__(self, device_id):
        dev_basic.RpxDevice.__init__(self, device_id)
        self._direction_flipped = False
        self._connection_string = ""
        self._motor_speed = 0

    @property
    def connection_string(self):
        return self._connection_string

    @rpx_util.getter(connection_string_description)
    def get_connection_string(self):
        return self._connection_string

    @rpx_util.setter(connection_string_description)
    def set_connection_string(self, connection_string):
        self._connection_string = connection_string
        return self._connection_string

    @property
    def direction_flipped(self):
        return self._direction_flipped

    @rpx_util.getter(direction_flipped_description)
    def get_direction_flipped(self):
        return str(self._direction_flipped)

    @rpx_util.setter(direction_flipped_description)
    def set_direction_flipped(self, direction_flipped):
        # self._direction_flipped = rpx_util.convert_to_bool(direction_flipped)
        return self.direction_flipped

    @property
    def motor_speed(self):
        return self._motor_speed

    @rpx_util.getter(motor_speed_description)
    def get_motor_speed(self):
        return self._motor_speed

    @rpx_util.setter(motor_speed_description)
    def set_motor_speed(self, speed):
        speed_set = self.drvr_set_motor_speed(speed)
        self._motor_speed = speed_set
        return self._motor_speed

    # @rpx_util.rpx_command("stop_motor")
    # def cmd_stop_motor(self):
    #   return "STOP COMMAND FOR %s" % self.device_id

    def drvr_get_motor_speed(self):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.drvr_get_motor_speed.__name__, self.device_id))

    def drvr_set_motor_speed(self, speed):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.drvr_set_motor_speed.__name__, self.device_id))

    def drvr_cmd_stop_motor(self):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.drvr_cmd_stop_motor.__name__, self.device_id))

