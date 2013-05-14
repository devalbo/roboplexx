__author__ = 'ajb'

# from roboplexx.rpx_util import *


# @rpx_device
class RpxDevice(object):

    persisted_rpx_property_descriptions = []

    def __init__(self, device_id):
        self.device_id = device_id

    # @rpx_command("rpx_activate")
    def activate(self):
        self.drvr_init()
        # self.rpx_apply_parameters()

    # @rpx_command("rpx_deactivate")
    def deactivate(self):
        return self.drvr_uninit()

    def drvr_init(self):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.drvr_init.__name__, self.device_id))

    def drvr_un_init(self):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.drvr_uninit.__name__, self.device_id))

    def drvr_apply_parameters(self, param_dict):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.drvr_apply_parameters.__name__, self.device_id))
