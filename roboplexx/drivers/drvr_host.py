import logging

from kombu import BrokerConnection, Exchange, Queue

from roboplexx import rpx_util, rpx_prop
from rpx_proto import rpx_pb2, descriptions_pb2
from roboplexx.devices import dev_basic

@rpx_util.rpx_device
class RpxHostDriver(dev_basic.RpxDevice):

    web_app_enabled_desc = rpx_prop.boolean_property_description("web_app_enabled", True)


    def __init__(self, host_id, rpx_password):
        dev_basic.RpxDevice.__init__(self, host_id)
        self._web_app_enabled = False
        self._web_app_host_name = ""
        self._web_app_port = -1
        self._debug_mode_on = False
        self._roboplexx_id = None
        self._properties_file = None
        self._rpx_password = rpx_password

        self.host_label = host_id
        self._host_rpx_props =  {}
        self._host_rpx_commands = {}

        self._device_paths = set()
        self._device_rpx_props =  {}
        self._device_rpx_commands = {}


    @property
    def host_id(self):
        return self.device_id

    @property
    def properties_file(self):
        return self._properties_file

    @properties_file.setter
    def properties_file(self, value):
        self._properties_file = value

    @property
    def roboplexx_id(self):
        return self._roboplexx_id

    @rpx_util.getter(rpx_prop.string_prop_desc("host_id"))
    def get_host_id(self):
        return self.device_id

    @property
    def rpx_password(self):
        return self._rpx_password

    @rpx_password.setter
    def rpx_password(self, value):
        self._rpx_password = value

    @property
    def web_app_enabled(self):
        return self._web_app_enabled

    @rpx_util.getter(web_app_enabled_desc)
    def get_web_app_enabled(self):
        return self._web_app_enabled

    @rpx_util.setter(web_app_enabled_desc)
    def set_web_app_enabled(self, value):
        self._web_app_enabled = value

    @property
    def web_app_host_name(self):
        return self._web_app_host_name

    @rpx_util.getter(rpx_prop.string_prop_desc("web_app_host_name"))
    def get_web_app_host_name(self):
        return self._web_app_host_name

    @rpx_util.setter(rpx_prop.string_prop_desc("web_app_host_name"))
    def set_web_app_host_name(self, value):
        self._web_app_host_name = value

    @property
    def web_app_port(self):
        return self._web_app_port

    @rpx_util.getter(rpx_prop.integer_prop_desc("web_app_port"))
    def get_web_app_port(self):
        return self._web_app_port

    @rpx_util.setter(rpx_prop.integer_prop_desc("web_app_port"))
    def set_web_app_port(self, value):
        self._web_app_port = value

    @property
    def debug_mode_on(self):
        return self._debug_mode_on

    @rpx_util.getter(rpx_prop.boolean_property_description("debug_mode_on"))
    def get_debug_mode_on(self):
        return self._debug_mode_on

    @rpx_util.setter(rpx_prop.boolean_property_description("debug_mode_on"))
    def set_debug_mode_on(self, value):
        self._debug_mode_on = value

    @rpx_util.getter(rpx_prop.string_prop_desc("roboplexx_id"))
    def get_roboplexx_id(self):
        return self._roboplexx_id

    @rpx_util.setter(rpx_prop.string_prop_desc("roboplexx_id"))
    def set_roboplexx_id(self, value):
        self._roboplexx_id = value

    @rpx_util.command("transmit_host_description")
    def transmit_host_description(self):
        self.register_with_webapp(self._web_app_url)

    def drvr_init(self):
        pass

    def drvr_uninit(self):
        pass

    def register_self_rpx_props_and_commands(self):
        rpx_prop_info, rpx_command_info = rpx_util.get_rpx_props_and_command_info(self)
        self._host_rpx_props = rpx_prop_info
        self._host_rpx_commands = rpx_command_info

    def register_device(self, device):

        device_path = tuple([device.device_id])
        if device_path in self._device_paths:
            raise Exception("Device already registered with host: %s" % device_path)

        self._device_paths.add(device_path)
        rpx_prop_info, rpx_command_info = rpx_util.get_rpx_props_and_command_info(device)
        self._device_rpx_props[device_path] = rpx_prop_info
        self._device_rpx_commands[device_path] = rpx_command_info

    def get_host_description(self):
        host_desc = descriptions_pb2.HostDescription()
        host_desc.hostId = self.host_id
        host_desc.hostLabel = self.host_label
        device_descriptions = host_desc.deviceDescriptions
        for device_path in self._device_paths:
            device_description = device_descriptions.add()
            device_description.deviceId = "->".join(device_path)
            device_description.deviceLabel = "->".join(device_path)
            device_description.deviceType = "->".join(device_path)
            for rpx_prop_id, rpx_prop in self._device_rpx_props[device_path].iteritems():
                prop_desc = device_description.devicePropertyDescriptions.add()
                prop_desc.CopyFrom(rpx_prop[0])
            for rpx_cmd_id, (dev_cmd_desc, dev_cmd_method) in self._device_rpx_commands[device_path].iteritems():
                cmd_desc = device_description.deviceCommandDescriptions.add()
                cmd_desc.CopyFrom(dev_cmd_desc)

        host_command_descriptions = host_desc.hostCommandDescriptions
        for cmd in self.__rpx_command_info__:
            host_command_description = host_command_descriptions.add()
            host_command_description.commandId = cmd
            host_command_description.commandLabel = cmd

        return host_desc

    def handle_message(self, body, rpx_message=None):
        print "Host body received >>", body
        # print "Host message received >>", rpx_message
        msg = rpx_pb2.RpxMessage()
        msg.ParseFromString(body)

        next_operation = msg.firstOperation
        while next_operation is not None:
            self.do_operation(next_operation)

            if next_operation.HasField("nextOperation"):
                next_operation = next_operation.nextOperation
            else:
                next_operation = None

    def do_operation(self, operation):
        for task in operation.tasks:
            self.do_task(task)

    def _validate_task_host(self, task):
        if task.hostId != self.host_id:
            msg = "Ignoring task for unidentified host: %s" % task.hostId
            logging.warning(msg)
            raise Exception(msg)

    def do_task(self, task):
        if task.taskType == rpx_pb2.Task.SetDevicePropertiesTaskType:
            task = task.setDevicePropertiesTask
            if task.hostId == self.host_id:
                device_path = tuple([d for d in task.devicePath])
                for prop in task.properties:
                    prop_desc, getter, setter = self._device_rpx_props[device_path][prop.propertyId]
                    setter(prop.doubleVal)

            else:
                logging.warning("Ignoring setDevicePropertiesTask for unidentified host: %s" % task.hostId)
            logging.info("%s >> %s >> %s" % (task.hostId, task.devicePath, task.properties))

        elif task.taskType == rpx_pb2.Task.DoHostCommandsTaskType:
            task = task.doHostCommandsTask
            self._validate_task_host(task)
            self._host_rpx_commands[task.commandId][1]()

        elif task.taskType == rpx_pb2.Task.DoDeviceCommandsTaskType:
            task = task.doDeviceCommandsTask
            if task.hostId == self.host_id:
                device_path = tuple([d for d in task.devicePath])
                cmd_fn = self._device_rpx_commands[device_path][task.commandId][1]
                cmd_fn()

        else:
            logging.warning("Unable to perform task type '%s' for host '%d'" % (task.taskType, task.hostId))

    def get_exchange_id(self):
        return 'RPX:RobotCmd:%s' % self.host_id

    def listen_command_queue(self, command_queue_url):

        def do_queue(command_queue_url):
            rpx_exchange = Exchange(self.get_exchange_id(),
                                    "direct",
                                    durable=True)
            command_queue = Queue(exchange=rpx_exchange)

            # connections
            with BrokerConnection(command_queue_url) as conn:

                # Declare the video queue so that the messages can be delivered.
                # It is a best practice in Kombu to have both publishers and
                # consumers declare the queue.
                command_queue(conn.channel()).declare()

                # consume
                with conn.Consumer(command_queue, callbacks=[self.handle_message]) as consumer:
                    # Process messages and handle events on all channels
                    while True:
                        conn.drain_events()

        from threading import Thread
        thread = Thread(target=do_queue, args=(command_queue_url, ))
        thread.start()

    def register_with_webapp(self, web_app_host):
        print "Registering with webapp at %s" % web_app_host

        import requests
        if web_app_host is not None:
            self._web_app_url = web_app_host
        register_url = "%s/api/register" % self._web_app_url
        response = requests.post(register_url)

        return response


    def checkin_with_web_app(self, web_app_host=None):
        print "Checking in with webapp at %s" % web_app_host

        import requests
        desc = self.get_host_description()
        desc_data = desc.SerializeToString()
        self._web_app_url = web_app_host
        checkin_url = "%s/api/checkin" % self._web_app_url
        response = requests.post(checkin_url, data=desc_data)
        return response
