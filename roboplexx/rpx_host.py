__author__ = 'ajb'

import logging
from rpx_proto import rpx_pb2, descriptions_pb2


class RpxHostDeprecated:

    def __init__(self, host_id, host_label=None):
        self.host_id = host_id
        self.host_label = host_id
        if host_label is not None:
            self.host_label = host_label
        self.device_paths = set()
        self.device_getters = {}
        self.device_setters = {}

    def register_device(self, device):

        device_path = tuple([device.device_id])
        if device_path in self.device_paths:
            raise Exception("Device already registered with host: %s" % device_path)

        self.device_paths.add(device_path)
        self.device_getters[device_path] = {}
        self.device_setters[device_path] = {}
        self.device_commands[device_path] = {}

        for method_name in dir(device):
            try:
                method = getattr(device, method_name)
                if hasattr(method, '_rpx_getter'):
                    proto_prop_desc, func_name = method._rpx_getter
                    self.device_getters[device_path][proto_prop_desc.propertyId] = method._rpx_getter
                    logging.info("Adding getter method %s for device path key: <%s> property key <%s>" % \
                                 (method._rpx_getter, device_path, proto_prop_desc.propertyId))

                if hasattr(method, '_rpx_setters'):
                    for prop_name, (func_name, prop_desc) in method._rpx_setters.iteritems():
                        self.device_setters[device_path][prop_name] = method
                        logging.info("Adding setter method %s for device path key: <%s> property key <%s>" % \
                                     (method, device_path, prop_name))

            except Exception, e:
                print e

    def get_host_description(self):
        host_desc = descriptions_pb2.HostDescription()
        host_desc.hostId = self.host_id
        host_desc.hostLabel = self.host_label
        device_descriptions = host_desc.deviceDescriptions
        for device_path in self.device_paths:
            device_description = device_descriptions.add()
            device_description.deviceId = "->".join(device_path)
            device_description.deviceLabel = "->".join(device_path)
            device_description.deviceType = "->".join(device_path)

        return host_desc

    def handle_message(self, rpx_message):
        msg = rpx_pb2.RpxMessage()
        msg.ParseFromString(rpx_message)

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

    def do_task(self, task):
        if task.taskType == rpx_pb2.Task.SetDevicePropertiesTaskType:
            task = task.setDevicePropertiesTask
            self._validate_task_host(task)
            device_path = tuple([d for d in task.devicePath])
            for prop in task.properties:
                self.device_setters[device_path][prop.propertyId](prop.doubleVal)
            logging.info("%s >> %s >> %s" % (task.hostId, task.devicePath, task.properties))

        elif task.taskType == rpx_pb2.DoHostCommandsTask:
            task = task.doHostCommandsTask
            self._validate_task_host(task)

        else:
            logging.warning("Unable to perform task type '%s' for host '%d'" % (task.taskType, task.hostId))

    def _validate_task_host(self, task):
        if task.hostId != self.host_id:
            msg = "Ignoring task for unidentified host: %s" % task.hostId
            logging.warning(msg)
            raise Exception(msg)
