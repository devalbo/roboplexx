from roboplexx import rpx_util, rpx_prop
from roboplexx.devices import dev_basic

@rpx_util.rpx_device
class DemoCamera(dev_basic.RpxDevice):

    def __init__(self, device_id):
        dev_basic.RpxDevice.__init__(self, device_id)

    @rpx_util.getter(rpx_prop.string_prop_desc("demo_camera_version"))
    def get_demo_camera_version(self):
        return "Demo Camera 1.2.3"

    @rpx_util.getter(rpx_prop.string_prop_desc("video_url"))
    def get_demo_camera_video_url(self):
        return "http://theoldrobots.com/images6/rob268.JPG"

    def drvr_init(self):
        pass

    def drvr_uninit(self):
        pass

