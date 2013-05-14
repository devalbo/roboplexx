__author__ = 'ajb'

import rpx_proto.descriptions_pb2

def boolean_property_description(prop_name, persist=False):
    prop_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    prop_desc.propertyId = prop_name
    prop_desc.propertyLabel = prop_name
    prop_desc.propertyType = rpx_proto.descriptions_pb2.BooleanType
    prop_desc.persist = persist
    return prop_desc

def string_prop_desc(prop_name, persist=False):
    prop_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    prop_desc.propertyId = prop_name
    prop_desc.propertyLabel = prop_name
    prop_desc.propertyType = rpx_proto.descriptions_pb2.StringType
    prop_desc.persist = persist
    return prop_desc

def integer_prop_desc(prop_name, persist=False):
    prop_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    prop_desc.propertyId = prop_name
    prop_desc.propertyLabel = prop_name
    prop_desc.propertyType = rpx_proto.descriptions_pb2.IntType
    prop_desc.persist = persist
    return prop_desc

def ranged_double_property_description(prop_name, min_val, max_val, persist=False):
    prop_desc = rpx_proto.descriptions_pb2.PropertyDescription()
    prop_desc.propertyId = prop_name
    prop_desc.propertyLabel = prop_name
    prop_desc.propertyType = rpx_proto.descriptions_pb2.DoubleType
    constraint = prop_desc.constraints
    prop_desc.persist = persist
    constraint.doubleTypeMinVal = min_val
    constraint.doubleTypeMaxVal = max_val
    return prop_desc

def command_description(cmd_name):
    cmd_desc = rpx_proto.descriptions_pb2.CommandDescription()
    cmd_desc.commandId = cmd_name
    cmd_desc.commandLabel = cmd_name
    return cmd_desc
