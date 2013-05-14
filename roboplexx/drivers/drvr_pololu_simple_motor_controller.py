from roboplexx import rpx_util, devices, rpx_prop

__author__ = 'ajb'

import serial

# @rpx_util.rpx_device
class PololuSimpleMotorController(devices.McBasic):

    def __init__(self, device_id):
        devices.McBasic.__init__(self, device_id)
        self._connection_string = "/dev/ttyACM0"
        self._connection = None
        self._motor_speed = 0;

    @rpx_util.getter(rpx_prop.string_prop_desc("firmware_version"))
    def get_firmware_version(self):
        return self._send_command("V")

    @rpx_util.getter(rpx_prop.string_prop_desc("connection_string"))
    def get_connection_string(self):
        return self._connection_string

    @rpx_util.setter(rpx_prop.string_prop_desc("connection_string"))
    def set_connection_string(self, connection_string):
        self._connection_string = value
        return self._connection_string

    def drvr_set_motor_speed(self, speed):
        _speed = int(round(float(speed)))
        if _speed < -100 or _speed > 100:
            raise rpx_util.RpxPropertyValidationError("Speed must be between -100 and 100 % (sent %s)" % _speed)

        cmd_direction = "F"
        if (self._direction_flipped and _speed >= 0) or (not self._direction_flipped and _speed < 0):
          cmd_direction = "R"
        _speed = abs(_speed)

        cmd = "%s%s%%" % (cmd_direction, _speed)
        self._send_command(cmd)

        self._motor_speed = speed
        return self._motor_speed

    def drvr_get_motor_speed(self):
        return self._motor_speed

    def drvr_init(self):
        self._connection = serial.Serial(self._connection_string, timeout=1.5)
        self._send_command("GO")

    def _send_command(self, command):
        self._connection.write("%s\n" % command)
        response = self._connection.readline()
        if response.startswith('.'):
          return response
        elif response.startswith('!'):
          raise rpx_util.RpxDevCommError("Motor error - stopped: %s" % response)
        elif response.startswith('?'):
          raise rpx_util.RpxDevCommError("Command not understood: %s" % command)
        else:
          raise rpx_util.RpxDevCommError("Unknown response: %s" % response)




#"GO"	Exit Safe-Start
#"F"	Motor Forward
#"R"	Motor Reverse
#"B"	Motor Brake
#"D"	Get Variable
#"L"	Set Motor Limit
#"V"	Get Firmware Version
#"X"	Stop Motor