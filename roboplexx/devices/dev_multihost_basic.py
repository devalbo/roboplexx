from roboplexx import rpx_util
from roboplexx.devices import dev_basic

__author__ = 'ajb'

# @rpx_util.rpx_device
class MultiHost(dev_basic.RpxDevice):

    def __init__(self, device_id):
        dev_basic.RpxDevice.__init__(self, device_id)

    def get_subdevices(self):
        raise NotImplementedError("%s not implemented for device ID '%s'" %
                                  (self.get_subdevices.__name__, self._device_id))

    def register_with_host(self, app):
        super(MultiHost, self).register_with_host(app)

        for subdevice in self.get_subdevices():
            for rpx_prop, rpx_prop_get_method_name in subdevice.rpx_getters.iteritems():
                getter_path = "/io/%s/%s/%s" % (self.device_id, subdevice.device_id, rpx_prop)
                endpoint_name = "io.%s.%s.prop.get.%s" % (self.device_id, subdevice.device_id, rpx_prop)
                app.add_url_rule(
                  getter_path,
                  view_func=rpx_util.RpxPropGetterView.as_view(endpoint_name,
                    dev_instance=subdevice, prop_get_method_name=rpx_prop_get_method_name)
                )

        for rpx_prop, rpx_prop_set_method_name in subdevice.rpx_setters.iteritems():
            setter_path = "/io/%s/%s/%s" % (self.device_id, subdevice.device_id, rpx_prop)
            endpoint_name = "io.%s.%s.prop.set.%s" % (self.device_id, subdevice.device_id, rpx_prop)
            app.add_url_rule(
              setter_path,
              view_func=rpx_util.RpxPropSetterView.as_view(endpoint_name,
                dev_instance=subdevice, prop_set_method_name=rpx_prop_set_method_name)
            )

        for rpx_command, rpx_command_method_name in subdevice.rpx_commands.iteritems():
            cmd_path = "/io/%s/%s/cmd/%s" % (self.device_id, subdevice.device_id, rpx_command)
            endpoint_name = "io.%s.%s.cmd.%s" % (self.device_id, subdevice.device_id, rpx_command)
            app.add_url_rule(
              cmd_path,
              endpoint=endpoint_name,
              view_func=getattr(subdevice, rpx_command_method_name),
              methods=['GET', 'POST']
            )