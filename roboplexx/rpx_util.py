from roboplexx import rpx_prop

__author__ = 'ajb'

# from flask.views import View
# from flask import request, render_template

import functools
import rpx_proto


def validate_property(prop_desc, prop):
    print "Desc >>", prop_desc
    p = property_to_py(prop)
    # for p in prop:
    #     print "Prop >>", p.propertyId

def get_property_name_paths(prop_desc, parent_path=[]):
    paths = parent_path[:]
    if prop_desc.type != rpx_proto.common_pb2.SubPropertiesType:
        paths.append(prop_desc.propertyId)
        return paths
    else:
        for child_prop_desc in prop_desc.subProperties:
            paths.append(get_property_name_paths(child_prop_desc, [prop_desc.propertyId]))
        return paths

def get_subproperty(property, subprop_id):
    for p in property.properties:
        if p.propertyId == subprop_id:
            return p

    raise Exception("Unable to find subproperty '%s'" % subprop_id)


def get_subproperty_value(property, subprop_id):
    for p in property.properties:
        if p.propertyId == subprop_id:
            if p.type == rpx_proto.common_pb2.DoubleType:
                return p.double
            elif p.type == rpx_proto.common_pb2.BooleanType:
                return p.bool
            elif p.type == rpx_proto.common_pb2.StringType:
                return p.string
            elif p.type == rpx_proto.common_pb2.IntType:
                return p.int
            elif p.type == rpx_proto.common_pb2.SubPropertiesType:
                return p.properties

    raise Exception("Unable to find subproperty '%s'" % subprop_id)


def properties_to_py(properties):
    d = {}
    for p in properties:
        val = property_to_py(p)

        if val is None:
            raise Exception("Unable to convert '%s' to " % (property.propertyId, property.type))

        d[p.propertyId] = val

    return d


def property_to_py(property):
    if property.type == rpx_proto.common_pb2.DoubleType:
        val = property.double
    elif property.type == rpx_proto.common_pb2.BooleanType:
        val = property.bool
    elif property.type == rpx_proto.common_pb2.StringType:
        val = property.string
    elif property.type == rpx_proto.common_pb2.IntType:
        val = property.int
    elif property.type == rpx_proto.common_pb2.SubPropertiesType:
        val = properties_to_py(property.properties)

    if val is None:
        raise Exception("Unable to convert '%s' to " % (property.propertyId, property.type))

    return val


def rpx_propstrval_to_py(prop_desc, prop_strval):
    val = None
    if prop_desc.propertyType == rpx_proto.descriptions_pb2.DoubleType:
        val = float(prop_strval)
    elif prop_desc.propertyType == rpx_proto.descriptions_pb2.BooleanType:
        val = bool(prop_strval)
    elif prop_desc.propertyType == rpx_proto.descriptions_pb2.StringType:
        val = prop_strval
    elif prop_desc.propertyType == rpx_proto.descriptions_pb2.IntType:
        val = int(prop_strval)

    if val is None:
        raise Exception("Unable to convert '%s' to %s" % (prop_desc.propertyId, prop_desc.propertyType))

    return val



def rpx_device(cls):
    # cls.rpx_getters = {}    # prop_name to (proto_prop, function name)
    # cls.rpx_setters = {}
    #
    # for method_name in dir(cls):
    #     method = getattr(cls, method_name)
    #     if hasattr(method, '_rpx_getter'):
    #         proto_prop = method._rpx_getter[0]
    #         rpx_getter = {proto_prop.propertyId: method._rpx_getter}
    #         cls.rpx_getters.update(rpx_getter)
    #     if hasattr(method, '_rpx_setters'):
    #         # proto_prop = method._rpx_setters[0]
    #         # rpx_setter = {proto_prop.propertyId: method._rpx_setter}
    #         cls.rpx_setters.update(method._rpx_setters)
    #
    # return cls

    rpx_descriptions = {}
    rpx_getters = {}
    rpx_setters = {}
    rpx_prop_info = {}

    rpx_command_info = {}

    for method_name in dir(cls):
        method = getattr(cls, method_name)
        if hasattr(method, "_rpx_getter"):
            prop_desc, func_name = method._rpx_getter
            prop_name = prop_desc.propertyId
            rpx_descriptions[prop_name] = prop_desc
            rpx_getters[prop_name] = method_name

        if hasattr(method, "_rpx_setters"):
            for prop_name, (set_method_name, prop_desc) in method._rpx_setters.iteritems():
                rpx_descriptions[prop_name] = prop_desc
                rpx_setters[prop_name] = set_method_name

        if hasattr(method, "_rpx_command_name"):
            rpx_command_info[method._rpx_command_name] = method_name

    for prop_name in rpx_descriptions:
        # it's OK to only have a getter, but not OK to only have a setter
        rpx_prop_info[prop_name] = (rpx_descriptions[prop_name],
                                    rpx_getters[prop_name],
                                    rpx_setters.get(prop_name, None))

    cls.__rpx_prop_info__ = rpx_prop_info
    cls.__rpx_command_info__ = rpx_command_info
    return cls



def get_rpx_props_and_command_info(rpx_device):

    rpx_descriptions = {}
    rpx_getters = {}
    rpx_setters = {}
    rpx_prop_info = {}

    rpx_command_info = {}

    for method_name in dir(rpx_device):
        method = getattr(rpx_device, method_name)
        if hasattr(method, "_rpx_getter"):
            prop_desc, func_name = method._rpx_getter
            prop_name = prop_desc.propertyId
            rpx_descriptions[prop_name] = prop_desc
            rpx_getters[prop_name] = method

        if hasattr(method, "_rpx_setters"):
            for prop_name, (set_method_name, prop_desc) in method._rpx_setters.iteritems():
                rpx_descriptions[prop_name] = prop_desc
                rpx_setters[prop_name] = method

        if hasattr(method, "_rpx_command_desc"):
            rpx_command_info[method._rpx_command_desc.commandId] = (method._rpx_command_desc, method)

    for prop_name in rpx_descriptions:
        # it's OK to only have a getter, but not OK to only have a setter
        rpx_prop_info[prop_name] = (rpx_descriptions[prop_name],
                                    rpx_getters[prop_name],
                                    rpx_setters.get(prop_name, None))

    return rpx_prop_info, rpx_command_info


# return {prop_names: (prop_desc, get_method_name, set_method_name)
# def get_rpx_descs_getters_setters(device):
#     rpx_descriptions = {}
#     rpx_getters = {}
#     rpx_setters = {}
#     retval = {}
#
#     for method_name in dir(device):
#         method = getattr(device, method_name)
#         if hasattr(method, "_rpx_getter"):
#             prop_desc, func_name = method._rpx_getter
#             prop_name = prop_desc.propertyId
#             # print ">>", prop_name, ":", func_name
#             rpx_descriptions[prop_name] = prop_desc
#             rpx_getters[prop_name] = func_name
#
#         if hasattr(method, "_rpx_setters"):
#             for prop_name, (set_method_name, prop_desc) in method._rpx_setters.iteritems():
#                 # if prop_name not in rpx_getters:
#                 #     raise Exception("Setter found for RPX property '%s', but getter does not exist" % prop_name)
#                 rpx_descriptions[prop_name] = prop_desc
#                 rpx_setters[prop_name] = set_method_name
#
#     # print "DESC", rpx_descriptions
#     for prop_name in rpx_descriptions:
#         retval[prop_name] = (rpx_descriptions[prop_name],
#                              rpx_getters[prop_name],
#                              rpx_setters.get(prop_name, None))
#
#     return retval


# # return {prop_names: prop_values}
# def get_persistent_rpx_properties(device):
#     rpx_props = {}
#     # for method_name in dir(device):
#     #     method = getattr(device, method_name)
#     #     if hasattr(method, "_rpx_setters"):
#     #         for prop_name, (set_method_name, prop_desc) in method._rpx_setters.iteritems():
#     #             if prop_desc.HasField("persist") and prop_desc.persist:
#     #                 for method_name_getter in dir(device):
#     #
#     #                 getter_func_name = device._rpx_getters[prop_name][1]
#     #                 getter_func = getattr(device, getter_func_name)
#     #                 prop_value = getter_func()
#     #                 rpx_props[prop_name] = prop_value
#
#     return rpx_props

        # func._rpx_setters.update({prop_name: func.__name__})

    # method = getattr(cls, method_name)
    #     if hasattr(method, '_rpx_getter'):
    #         proto_prop = method._rpx_getter[0]
    #         rpx_getter = {proto_prop.propertyId: method._rpx_getter}
    #         cls.rpx_getters.update(rpx_getter)
    #     if hasattr(method, '_rpx_setters'):
    #         # proto_prop = method._rpx_setters[0]
    #         # rpx_setter = {proto_prop.propertyId: method._rpx_setter}
    #         cls.rpx_setters.update(method._rpx_setters)
    #
    # return cls



def validate_property(prop_desc, prop_value):
    if prop_desc.propertyType == rpx_proto.descriptions_pb2.DoubleType:
        # value = prop_value.doubleVal
        value = prop_value
        assert type(value) == float
        if prop_desc.HasField("constraints"):
            if prop_desc.constraints.HasField("doubleTypeMinVal"):
                assert value >= prop_desc.constraints.doubleTypeMinVal
            if prop_desc.constraints.HasField("doubleTypeMaxVal"):
                assert value <= prop_desc.constraints.doubleTypeMaxVal



# def old_getter(prop_desc):
#     def wrapper(func):
#         func._rpx_getter = (prop_desc, func.__name__)
#         return func
#     return wrapper
#
# def old_setter(prop_desc):
#     def wrapper(func):
#         func._rpx_setter = (prop_desc, func.__name__)
#
#         # def validator(instance, prop_value):
#         #     validate_property(prop_desc, prop_value)
#         #     return func(instance, prop_value)
#         # return validator
#
#         return func
#
#     return wrapper


def command(rpx_command_name):
    def wrapper(func):
        cmd_desc = rpx_prop.command_description(rpx_command_name)
        func._rpx_command_desc = cmd_desc
        return func
    return wrapper


def getter(prop_desc):
    def wrapper(func):
        func._rpx_getter = (prop_desc, func.__name__)
        return func
    return wrapper


# def old_setter(prop_desc):
#     def wrapper(func):
#         func._rpx_setter = (prop_desc, func.__name__)
#
#         # def validator(instance, prop_value):
#         #     validate_property(prop_desc, prop_value)
#         #     return func(instance, prop_value)
#         # return validator
#
#         return func
#
#     return wrapper

# def dict_setter(**prop_descs):
#     def decorator(func):
#         import inspect
#         func._rpx_setters = {}  # prop_name key to (function name, property description)
#         argspec = inspect.getargspec(func)
#         for prop_name in prop_descs:
#             if prop_name not in argspec[0]:
#                 raise Exception("Property descriptions and method argument mismatch: '%s'" % prop_name)
#             func._rpx_setters.update({prop_name: (func.__name__, prop_descs[prop_name])})
#
#         @functools.wraps(func)
#         def wrapper(self, *args, **kwargs):
#             for k, value in kwargs.iteritems():
#                 prop_desc = prop_descs[k]
#                 validate_property(prop_desc, value)
#             func(self, *args, **kwargs)
#         return wrapper
#
#     return decorator

def setter(*prop_descs):
    def decorator(func):
        func._rpx_setters = {}  # prop_name key to (function name, property description)

        if len(prop_descs) == 1:
            prop_desc = prop_descs[0]
            prop_name = prop_desc.propertyId
            func._rpx_setters.update({prop_name: (func.__name__, prop_desc)})

            @functools.wraps(func)
            def wrapper(self, value):
                validate_property(prop_descs[0], value)
                func(self, value)
            return wrapper

        else:
            import inspect
            prop_desc_dict = {}
            argspec = inspect.getargspec(func)
            for prop_desc in prop_descs:
                prop_name = prop_desc.propertyId
                if prop_name not in argspec[0]:
                    raise Exception("No such method argument for property: '%s'" % prop_name)
                func._rpx_setters.update({prop_name: (func.__name__, prop_desc)})
                prop_desc_dict[prop_name] = prop_desc

            @functools.wraps(func)
            def wrapper(self, **kwargs):
                for k, value in kwargs.iteritems():
                    prop_desc = prop_desc_dict[k]
                    validate_property(prop_desc, value)
                func(self, **kwargs)
            return wrapper

    return decorator

# class RpxPropGetterView(View):
#     methods = ["GET"]
#
#     def __init__(self, dev_instance, prop_get_method_name, prop_description, prop_set_url, prop_label):
#         self._device_instance = dev_instance
#         self._prop_get_method_name = prop_get_method_name
#         self._prop_description = prop_description
#         self._prop_set_url = prop_set_url
#         self._prop_label = prop_label
#         self._prop_form_names = get_property_name_paths(self._prop_description)
#
#     def dispatch_request(self):
#         values = getattr(self._device_instance, self._prop_get_method_name)()
#         return render_template("multi_prop.html",
#                                values=values,
#                                # prop_names="",
#                                prop_set_url=self._prop_set_url,
#                                prop_label=self._prop_label)
#
#
# class RpxPropSetterView(View):
#     methods = ["POST"]
#
#     def __init__(self, dev_instance, prop_set_method_name, prop_description):
#         self._device_instance = dev_instance
#         self._prop_set_method_name = prop_set_method_name
#         self._prop_description = prop_description
#         self._prop_form_names = get_property_name_paths(self._prop_description)
#
#     def dispatch_request(self):
#         value = request.form['value']
#         return getattr(self._device_instance, self._prop_set_method_name)(value)


# class RpxMultiPropGetterView(View):
#   methods = ["GET"]
#
#   def __init__(self, dev_instance, prop_get_method_name, prop_set_url):
#     self._device_instance = dev_instance
#     self._prop_get_method_name = prop_get_method_name
#     self._prop_set_url = prop_set_url
#
#   def dispatch_request(self):
#     values = getattr(self._device_instance, self._prop_get_method_name)()
#     return render_template("multi_prop.html",
#       values=values,
#       prop_set_url=self._prop_set_url,
#     )
#
# class RpxMultiPropSetterView(View):
#   methods = ["POST"]
#
#   def __init__(self, dev_instance, prop_set_method_name, multi_names, prop_set_url):
#     self._device_instance = dev_instance
#     self._prop_set_method_name = prop_set_method_name
#     self._multi_names = multi_names
#     self._prop_set_url = prop_set_url
#
#   def dispatch_request(self):
#     values = {}
#     for multi_name in self._multi_names:
#       values[multi_name] = request.form[multi_name]
#     response_values = getattr(self._device_instance, self._prop_set_method_name)(**values)
#     return render_template("multi_prop.html",
#       values=response_values,
#       prop_set_url=self._prop_set_url
#       )


def convert_to_bool(exp):
    return exp.lower() in ("yes", "true", "t", "1")

class RpxDevNotInitializedError(Exception):
    pass

class RpxDevCommError(Exception):
    pass

class RpxPropertyValidationError(Exception):
    pass

def add_double_property(cmd, property_id, property_value):
    p = cmd.properties.add()
    p.type = rpx_proto.common_pb2.DoubleType
    p.propertyId = property_id
    p.double = property_value
    return p


def apply_rpx_property_string_value_to_device(device, rpx_prop_id, rpx_prop_value):
    """Convert string to appropriate type for RPX property, then apply it."""
    rpx_description, rpx_getter, rpx_setter = device.__rpx_prop_info__[rpx_prop_id]
    rpx_typed_prop_val = rpx_propstrval_to_py(rpx_description, rpx_prop_value)
    # setattr(device, rpx_prop_id, rpx_typed_prop_val)
    if rpx_setter is not None:
        # print "Applying", rpx_prop_id, rpx_prop_value
        getattr(device, rpx_setter)(rpx_typed_prop_val)
    else:
        print "No setter available on %s for '%s'" % (device, rpx_prop_id)


# rpx_info[prop_name] = (rpx_descriptions[prop_name],
#                                rpx_getters[prop_name],
#                                rpx_setters.get(prop_name, None))