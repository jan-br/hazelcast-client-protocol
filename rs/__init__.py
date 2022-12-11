import fnmatch
import os

rs_reserved_keywords = {
    'as',
    'use',
    'extern crate',
    'break',
    'const',
    'continue',
    'crate',
    'else',
    'if',
    'if let',
    'enum',
    'extern',
    'false',
    'fn',
    'for',
    'if',
    'impl',
    'in',
    'for',
    'let',
    'loop',
    'match',
    'mod',
    'move',
    'mut',
    'pub',
    'impl',
    'ref',
    'return',
    'Self',
    'self',
    'static',
    'struct',
    'super',
    'trait',
    'true',
    'type',
    'unsafe',
    'use',
    'where',
    'while',
    'abstract',
    'alignof',
    'become',
    'box',
    'do',
    'final',
    'macro',
    'offsetof',
    'override',
    'priv',
    'proc',
    'pure',
    'sizeof',
    'typeof',
    'unsized',
    'virtual',
    'yield'
}


class ImportPathHolder:
    def __init__(self, name, path, is_builtin_codec=False,
                 is_custom_codec=False, is_internal_file=True,
                 import_as_wildcard=False):
        self.name = name
        self.path = path
        self.is_builtin_codec = is_builtin_codec
        self.is_custom_codec = is_custom_codec
        self.is_internal_file = is_internal_file
        self.import_as_wildcard = import_as_wildcard

    def get_import_statement(self, is_called_from_custom_codec):
        codec_path: str = self.path
        if self.is_builtin_codec:
            codec_path = "codec_builtin::" + codec_path
        elif self.is_custom_codec:
            codec_path = "codec::custom::" + codec_path

        if self.is_internal_file:
            codec_path = "crate::" + codec_path

        return "use {}::{};".format(codec_path, self.name)

        # codec_path: str = self.path
        # if self.is_internal_file:
        #     if is_called_from_custom_codec:
        #         if self.is_builtin_codec:
        #             path = 'crate::%s'
        #         elif self.is_custom_codec:
        #             codec_path = codec_path.replace('custom::', '', 1)
        #             path = 'crate::%s'
        #         else:
        #             path = 'crate::%s'
        #     else:
        #         if self.is_builtin_codec or self.is_custom_codec:
        #             path = 'crate::%s'
        #         else:
        #             path = 'crate::%s'
        #     statement = 'use ' + path + "::%s;"
        #     # statement = 'import {%s} from \'' + path + '\';'
        # else:
        #     if self.import_as_wildcard:
        #         statement = 'use %s::%s::*;'
        #         # statement = 'import * as %s from \'%s\';'
        #     else:
        #         statement = 'use %s::%s;'
        #         # statement = 'import {%s} from \'%s\';'
        # return statement % (codec_path, self.name)




class PathHolders:
    FieldDescriptor = ImportPathHolder("FieldDescriptor", "serialization::generic_record::field_descriptor", is_internal_file=True)
    FieldDescriptorCodec = ImportPathHolder("FieldDescriptorCodec", "field_descriptor_codec", is_internal_file=True, is_custom_codec=True)
    List = ImportPathHolder('Vec', 'std::vec', is_internal_file=False)
    SchemaCodec = ImportPathHolder('SchemaCodec', 'schema_codec', is_custom_codec=True)
    Schema = ImportPathHolder('Schema', 'serialization::schema', is_internal_file=True)
    UUID = ImportPathHolder('Uuid', 'uuid', is_internal_file=False, import_as_wildcard=False)
    Data = ImportPathHolder('HeapData', 'serialization::heap_data')
    DataCodec = ImportPathHolder('DataCodec', 'data_codec', is_builtin_codec=True)
    ByteArrayCodec = ImportPathHolder('ByteArrayCodec', 'byte_array_codec', is_builtin_codec=True)
    LongArrayCodec = ImportPathHolder('LongArrayCodec', 'long_array_codec', is_builtin_codec=True)
    Address = ImportPathHolder('Address', 'connection::address')
    AddressCodec = ImportPathHolder('AddressCodec', 'address_codec', is_custom_codec=True)
    ErrorHolder = ImportPathHolder('ErrorHolder', 'protocol')
    ErrorHolderCodec = ImportPathHolder('ErrorHolderCodec', 'custom', is_custom_codec=True)
    StackTraceElement = ImportPathHolder('StackTraceElement', 'protocol')
    StackTraceElementCodec = ImportPathHolder('StackTraceElementCodec', 'custom', is_custom_codec=True)
    SimpleEntryView = ImportPathHolder('SimpleEntryView', 'core')
    SimpleEntryViewCodec = ImportPathHolder('SimpleEntryViewCodec', 'custom', is_custom_codec=True)
    RaftGroupId = ImportPathHolder('RaftGroupId', 'proxy::cpsubsystem')
    RaftGroupIdCodec = ImportPathHolder('RaftGroupIdCodec', 'custom', is_custom_codec=True)
    DistributedObjectInfo = ImportPathHolder('DistributedObjectInfo', 'core::distributed_object_info')
    DistributedObjectInfoCodec = ImportPathHolder('DistributedObjectInfoCodec', 'DistributedObjectInfoCodec', is_custom_codec=True)
    MemberInfo = ImportPathHolder('MemberInfo', 'core::member::info')
    MemberInfoCodec = ImportPathHolder('MemberInfoCodec', 'member_info_codec', is_custom_codec=True)
    MemberVersion = ImportPathHolder('MemberVersion', 'core::member::version')
    MemberVersionCodec = ImportPathHolder('MemberVersionCodec', 'member_version_codec', is_custom_codec=True)
    EndpointQualifier = ImportPathHolder('EndpointQualifier', 'core::member::endpoint')
    EndpointQualifierCodec = ImportPathHolder('EndpointQualifierCodec', 'endpoint_qualifier_codec', is_custom_codec=True)
    StringCodec = ImportPathHolder('StringCodec', 'string_codec', is_builtin_codec=True)
    ListLongCodec = ImportPathHolder('ListLongCodec', 'codec_builtin', is_builtin_codec=True)
    ListIntegerCodec = ImportPathHolder('ListIntegerCodec', 'codec_builtin', is_builtin_codec=True)
    ListUUIDCodec = ImportPathHolder('ListUUIDCodec', 'codec_builtin', is_builtin_codec=True)
    ListDataCodec = ImportPathHolder('ListDataCodec', 'codec_builtin', is_builtin_codec=True)
    ListMultiFrameCodec = ImportPathHolder('ListMultiFrameCodec', 'list_multi_frame_codec', is_builtin_codec=True)
    EntryListCodec = ImportPathHolder('EntryListCodec', 'entry_list_codec', is_builtin_codec=True)
    EntryListLongByteArrayCodec = ImportPathHolder('EntryListLongByteArrayCodec', 'codec_builtin', is_builtin_codec=True)
    EntryListIntegerUUIDCodec = ImportPathHolder('EntryListIntegerUUIDCodec', 'codec_builtin', is_builtin_codec=True)
    EntryListIntegerLongCodec = ImportPathHolder('EntryListIntegerLongCodec', 'codec_builtin', is_builtin_codec=True)
    EntryListIntegerIntegerCodec = ImportPathHolder('EntryListIntegerIntegerCodec', 'codec_builtin', is_builtin_codec=True)
    EntryListUUIDLongCodec = ImportPathHolder('EntryListUUIDLongCodec', 'codec_builtin', is_builtin_codec=True)
    EntryListUUIDUUIDCodec = ImportPathHolder('EntryListUUIDUUIDCodec', 'codec_builtin', is_builtin_codec=True)
    EntryListUUIDListIntegerCodec = ImportPathHolder('EntryListUUIDListIntegerCodec', 'entry_list_uuid_list_integer_codec', is_builtin_codec=True)
    MapCodec = ImportPathHolder('MapCodec', 'map_codec', is_builtin_codec=True)
    CodecUtil = ImportPathHolder('CodecUtil', 'codec_util', is_builtin_codec=True)
    IndexConfig = ImportPathHolder('InternalIndexConfig', 'config')
    IndexConfigCodec = ImportPathHolder('IndexConfigCodec', 'custom', is_custom_codec=True)
    BitmapIndexOptions = ImportPathHolder('InternalBitmapIndexOptions', 'config')
    BitmapIndexOptionsCodec = ImportPathHolder('BitmapIndexOptionsCodec', 'custom', is_custom_codec=True)
    PagingPredicateHolder = ImportPathHolder('PagingPredicateHolder', 'protocol')
    PagingPredicateHolderCodec = ImportPathHolder('PagingPredicateHolderCodec', 'custom', is_custom_codec=True)
    AnchorDataListHolder = ImportPathHolder('AnchorDataListHolder', 'protocol')
    AnchorDataListHolderCodec = ImportPathHolder('AnchorDataListHolderCodec', 'custom', is_custom_codec=True)

    SqlError = ImportPathHolder('SqlError', 'sql')
    SqlErrorCodec = ImportPathHolder('SqlErrorCodec', 'custom', is_custom_codec=True)
    SqlQueryId = ImportPathHolder('SqlQueryId', 'sql')
    SqlQueryIdCodec = ImportPathHolder('SqlQueryIdCodec', 'custom', is_custom_codec=True)
    SqlColumnMetadata = ImportPathHolder('SqlColumnMetadataImpl', 'sql')
    SqlColumnMetadataCodec = ImportPathHolder('SqlColumnMetadataCodec', 'custom', is_custom_codec=True)
    SqlPage = ImportPathHolder('SqlPage', 'sql')
    SqlPageCodec = ImportPathHolder('SqlPageCodec', 'codec_builtin', is_builtin_codec=True)
    HazelcastJsonValue = ImportPathHolder('HazelcastJsonValue', 'core')
    HazelcastJsonValueCodec = ImportPathHolder('HazelcastJsonValueCodec', 'custom', is_custom_codec=True)

import_paths = {
    'FieldDescriptor': [PathHolders.FieldDescriptor, PathHolders.FieldDescriptorCodec],
    'Schema': [PathHolders.Schema, PathHolders.SchemaCodec],
    'CodecUtil': PathHolders.CodecUtil,
    'UUID': [PathHolders.UUID],
    'longArray': [PathHolders.LongArrayCodec],
    'byteArray': [PathHolders.ByteArrayCodec],
    'String': [PathHolders.StringCodec],
    'Data': [PathHolders.Data, PathHolders.DataCodec],
    'Address': [PathHolders.Address, PathHolders.AddressCodec],
    'ErrorHolder': [PathHolders.ErrorHolder, PathHolders.ErrorHolderCodec],
    'StackTraceElement': [PathHolders.StackTraceElement, PathHolders.StackTraceElementCodec],
    'SimpleEntryView': [PathHolders.SimpleEntryView, PathHolders.Data, PathHolders.SimpleEntryViewCodec],
    'RaftGroupId': [PathHolders.RaftGroupId, PathHolders.RaftGroupIdCodec],
    'DistributedObjectInfo': [PathHolders.DistributedObjectInfo, PathHolders.DistributedObjectInfoCodec],
    'MemberInfo': [PathHolders.MemberInfo, PathHolders.MemberInfoCodec],
    'MemberVersion': [PathHolders.MemberVersion, PathHolders.MemberVersionCodec],
    'EndpointQualifier': [PathHolders.EndpointQualifier, PathHolders.EndpointQualifierCodec],
    'List_FieldDescriptor': [PathHolders.List, PathHolders.FieldDescriptor, PathHolders.FieldDescriptorCodec],
    'List_Long': [PathHolders.ListLongCodec],
    'List_Integer': [PathHolders.ListIntegerCodec],
    'List_UUID': [PathHolders.UUID, PathHolders.ListUUIDCodec],
    'List_String': [PathHolders.ListMultiFrameCodec, PathHolders.StringCodec],
    'List_Data': [PathHolders.Data, PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    'ListCN_Data': [PathHolders.Data, PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    'List_MemberInfo': [PathHolders.MemberInfo, PathHolders.ListMultiFrameCodec, PathHolders.MemberInfoCodec],
    'List_DistributedObjectInfo': [PathHolders.DistributedObjectInfo, PathHolders.ListMultiFrameCodec,
                                   PathHolders.DistributedObjectInfoCodec],
    'List_StackTraceElement': [PathHolders.StackTraceElement, PathHolders.ListMultiFrameCodec,
                               PathHolders.StackTraceElementCodec],
    'EntryList_String_String': [PathHolders.EntryListCodec, PathHolders.StringCodec],
    'EntryList_String_byteArray': [PathHolders.EntryListCodec, PathHolders.StringCodec, PathHolders.ByteArrayCodec],
    'EntryList_Long_byteArray': [PathHolders.EntryListLongByteArrayCodec],
    'EntryList_Integer_UUID': [PathHolders.EntryListIntegerUUIDCodec, PathHolders.UUID],
    'EntryList_Integer_Long': [PathHolders.EntryListIntegerLongCodec],
    'EntryList_Integer_Integer': [PathHolders.EntryListIntegerIntegerCodec],
    'EntryList_UUID_Long': [PathHolders.EntryListUUIDLongCodec, PathHolders.UUID],
    'EntryList_String_EntryList_Integer_Long': [PathHolders.EntryListCodec, PathHolders.StringCodec,
                                                PathHolders.EntryListIntegerLongCodec],
    'EntryList_UUID_UUID': [PathHolders.EntryListUUIDUUIDCodec, PathHolders.UUID],
    'EntryList_UUID_List_Integer': [PathHolders.List, PathHolders.EntryListUUIDListIntegerCodec, PathHolders.UUID],
    'EntryList_Data_Data': [PathHolders.EntryListCodec, PathHolders.DataCodec, PathHolders.Data],
    'EntryList_Data_List_Data': [PathHolders.EntryListCodec, PathHolders.DataCodec, PathHolders.ListDataCodec,
                                 PathHolders.Data],
    'Map_String_String': [PathHolders.MapCodec, PathHolders.StringCodec],
    "Map_EndpointQualifier_Address": [PathHolders.MapCodec, PathHolders.EndpointQualifierCodec,
                                      PathHolders.AddressCodec],
    'IndexConfig': [PathHolders.IndexConfig, PathHolders.IndexConfigCodec],
    'ListIndexConfig': [PathHolders.IndexConfig, PathHolders.IndexConfigCodec, PathHolders.ListMultiFrameCodec],
    'BitmapIndexOptions': [PathHolders.BitmapIndexOptions, PathHolders.BitmapIndexOptionsCodec],
    'AnchorDataListHolder': [PathHolders.AnchorDataListHolder, PathHolders.AnchorDataListHolderCodec],
    'PagingPredicateHolder': [PathHolders.PagingPredicateHolder, PathHolders.PagingPredicateHolderCodec],
    'SqlColumnMetadata': [PathHolders.SqlColumnMetadata, PathHolders.SqlColumnMetadataCodec],
    'SqlError': [PathHolders.SqlErrorCodec, PathHolders.SqlError],
    'SqlQueryId': [PathHolders.SqlQueryIdCodec, PathHolders.SqlQueryId],
    'List_SqlColumnMetadata': [PathHolders.SqlColumnMetadataCodec, PathHolders.SqlColumnMetadata, PathHolders.ListMultiFrameCodec],
    'SqlPage': [PathHolders.SqlPage, PathHolders.SqlPageCodec],
    'HazelcastJsonValue': [PathHolders.HazelcastJsonValue, PathHolders.HazelcastJsonValueCodec]
}



rs_ignore_service_list = list([
    "CacheEventData",
    "CacheSimpleEntryListenerConfig",
    "ErrorHolder",
    "EventJournalConfig",
    "EvictionConfigHolder",
    "HotRestartConfig",
    "ListenerConfigHolder",
    "AttributeConfig",
    "IndexConfig",
    "BitmapIndexOptions",
    "BTreeIndexConfig",
    "MapStoreConfigHolder",
    "MerkleTreeConfig",
    "NearCacheConfigHolder",
    "NearCachePreloaderConfig",
    "PredicateConfigHolder",
    "QueryCacheConfigHolder",
    "QueryCacheEventData",
    "QueueStoreConfigHolder",
    "RingbufferStoreConfigHolder",
    "ScheduledTaskHandler",
    "SimpleEntryView",
    "StackTraceElement",
    "DurationConfig",
    "TimedExpiryPolicyFactoryConfig",
    "WanReplicationRef",
    "Xid",
    "MergePolicyConfig",
    "CacheConfigHolder",
    "ClientBwListEntry",
    "EndpointQualifier",
    "MemberVersion",
    "MCEvent",
    "AnchorDataListHolder",
    "PagingPredicateHolder",
    "SqlQueryId",
    "SqlError",
    "SqlColumnMetadata",
    "CPMember",
    "MigrationState",
    "Schema",
    "HazelcastJsonValue",
    "DataPersistenceConfig",
    "Capacity",
    "MemoryTierConfig",
    "DiskTierConfig",
    "TieredStoreConfig",
    "SqlSummary",
    "JobAndSqlSummary",
    "RaftGroupId"
])


def rs_get_import_path_holders(param_type):
    return import_paths.get(param_type, [])

for root, dirnames, filenames in os.walk('./protocol-definitions'):
    for filename in fnmatch.filter(filenames, '*.yaml'):
        # append to rs_ignore_service_list
        rs_ignore_service_list.append(filename[:-5])

rs_ignore_service_list.remove("Map")
rs_ignore_service_list.remove("Client")
rs_ignore_service_list.remove("Schema")
rs_ignore_service_list.remove("MemberVersion")
rs_ignore_service_list.remove("EndpointQualifier")
print(rs_ignore_service_list)

def rs_types_encode(key):
    rs_type = _rs_types[key]
    if rs_type == 'NA':
        raise NotImplementedError("MissingTypeMapping")
    return rs_type


def rs_types_decode(key):
    rs_type = _rs_types[key]
    if rs_type == 'NA':
        raise NotImplementedError("MissingTypeMapping")
    return rs_type


def rs_escape_keyword(value):
    if value not in rs_reserved_keywords:
        return value
    return "_" + value

_rs_types = {
    "boolean": "bool",
    "int": "i32",
    "long": "i64",
    "byte": "u8",
    "Integer": "i32",
    "Long": "i64",
    "UUID": "Uuid",

    "List_FieldDescriptor": "Vec<FieldDescriptor>",
    "Schema": "Schema",
    "List_Schema": "Vec<Schema>",
    "longArray": "Long[]",
    "byteArray": "Buffer",
    "String": "String",
    "Data": "HeapData",
    "Address": "Address",
    "FieldDescriptor": "FieldDescriptor",
    "ErrorHolder": "ErrorHolder",
    "StackTraceElement": "StackTraceElement",
    "SimpleEntryView": "SimpleEntryView<Data, Data>",
    "RaftGroupId": "RaftGroupId",
    "WanReplicationRef": "NA",
    "HotRestartConfig": "NA",
    "EventJournalConfig": "NA",
    "MerkleTreeConfig": "NA",
    "TimedExpiryPolicyFactoryConfig": "NA",
    "MapStoreConfigHolder": "NA",
    "QueueStoreConfigHolder": "NA",
    "RingbufferStoreConfigHolder": "NA",
    "NearCacheConfigHolder": "NA",
    "EvictionConfigHolder": "NA",
    "NearCachePreloaderConfig": "NA",
    "PredicateConfigHolder": "NA",
    "DurationConfig": "NA",
    "MergePolicyConfig": "NA",
    "CacheConfigHolder": "NA",
    "CacheEventData": "NA",
    "QueryCacheConfigHolder": "NA",
    "DistributedObjectInfo": "DistributedObjectInfo",
    "IndexConfig": "InternalIndexConfig",
    "BitmapIndexOptions": "InternalBitmapIndexOptions",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "MemberInfo": "MemberInfo",
    "MemberVersion": "MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "AnchorDataListHolder",
    "PagingPredicateHolder": "PagingPredicateHolder",
    "EndpointQualifier": "EndpointQualifier",
    "SqlQueryId": "SqlQueryId",
    "SqlError": "SqlError",
    "SqlColumnMetadata": "SqlColumnMetadataImpl",
    'SqlPage': 'SqlPage',
    'HazelcastJsonValue': 'HazelcastJsonValue',
    "CPMember": "NA",
    "MigrationState": "NA",

    "List_Long": "Long[]",
    "List_Integer": "number[]",
    "List_UUID": "UUID[]",
    "List_String": "Vec<String>",
    "List_Xid": "NA",
    "List_Data": "Data[]",
    "ListCN_Data": "Data[]",
    "List_ListCN_Data": "NA",
    "List_MemberInfo": "Vec<MemberInfo>",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "Vec<DistributedObjectInfo>",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "IndexConfig[]",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "StackTraceElement[]",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_SqlColumnMetadata": "SqlColumnMetadataImpl[]",

    "EntryList_String_String": "Vec<(String, String)>",
    "EntryList_String_byteArray": "Vec<(String, Vec<u8>)>",
    "EntryList_Long_byteArray": "Array<[Long, number[]]>",
    "EntryList_Integer_UUID": "Array<[number, UUID]>",
    "EntryList_Integer_Long": "Array<[number, Long]>",
    "EntryList_Integer_Integer": "Vec<(i32, i32)>",
    "EntryList_UUID_Long": "Vec<(Uuid, i64)>",
    "EntryList_String_EntryList_Integer_Long": "Array<[string, Array<[number, Long]>]>",
    "EntryList_UUID_UUID": "Array<[UUID, UUID]>",
    "EntryList_UUID_List_Integer": "Vec<(Uuid, Vec<i32>)>",
    "EntryList_Data_Data": "Array<[Data, Data]>",
    "EntryList_Data_List_Data": "Array<[Data, Data[]]>",

    "Map_String_String": "Map<string, string>",
    "Map_EndpointQualifier_Address": "Map<EndpointQualifier, AddressImpl>",

    "Set_UUID": "NA",
}