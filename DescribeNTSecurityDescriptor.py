#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : DescribeNTSecurityDescriptor.py
# Author             : Podalirius (@podalirius_)
# Date created       : 20 Nov 2023

import argparse
import binascii
from enum import Enum, IntFlag
import io
import os
import random
import re
import struct
import sys


class ExtendedRights(Enum):
    """
    ExtendedRights is an enumeration of GUIDs representing various extended rights in Active Directory.
    These rights are associated with specific operations that can be performed on AD objects.
    Each entry in this enumeration maps a human-readable name to the corresponding GUID of the extended right.
    These GUIDs are used in Access Control Entries (ACEs) to grant or deny these rights to security principals (users, groups, etc.).

    The rights include, but are not limited to, the ability to create or delete specific types of child objects,
    force password resets, read/write specific properties, and more. They play a crucial role in defining
    the security model of Active Directory by allowing fine-grained access control to objects.

    The GUIDs are defined by Microsoft and can be found in the Microsoft documentation and technical specifications.

    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/443fe66f-c9b7-4c50-8c24-c708692bbf1d
    """

    # 
    ABANDON_REPLICATION = "ee914b82-0a98-11d1-adbb-00c04fd8d5cd"
	#
    ADD_GUID = "440820ad-65b4-11d1-a3da-0000f875ae0d"
	#
    ALLOCATE_RIDS = "1abd7cf8-0a99-11d1-adbb-00c04fd8d5cd"
	#
    ALLOWED_TO_AUTHENTICATE = "68b1d179-0d15-4d4f-ab71-46152e79a7bc"
	#
    APPLY_GROUP_POLICY = "edacfd8f-ffb3-11d1-b41d-00a0c968f939"
    # 
    CERTIFICATE_ENROLLMENT = "0e10c968-78fb-11d2-90d4-00c04f79dc55"
	# 
    CHANGE_DOMAIN_MASTER = "014bf69c-7b3b-11d1-85f6-08002be74fab"
	# 
    CHANGE_INFRASTRUCTURE_MASTER = "cc17b1fb-33d9-11d2-97d4-00c04fd8d5cd"
	# 
    CHANGE_PDC = "bae50096-4752-11d1-9052-00c04fc2d4cf"
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/fcb2b5e7-302f-43cb-8adf-4c9cd9423178
    CHANGE_RID_MASTER = "d58d5f36-0a98-11d1-adbb-00c04fd8d5cd"
	# 
    CHANGE_SCHEMA_MASTER = "e12b56b6-0a95-11d1-adbb-00c04fd8d5cd"
	# 
    CREATE_INBOUND_FOREST_TRUST = "e2a36dc9-ae17-47c3-b58b-be34c55ba633"
	# 
    DO_GARBAGE_COLLECTION = "fec364e0-0a98-11d1-adbb-00c04fd8d5cd"
	# 
    DOMAIN_ADMINISTER_SERVER = "ab721a52-1e2f-11d0-9819-00aa0040529b"
	# 
    DS_CHECK_STALE_PHANTOMS = "69ae6200-7f46-11d2-b9ad-00c04f79f805"
	# 
    DS_CLONE_DOMAIN_CONTROLLER = "3e0f7e18-2c7a-4c10-ba82-4d926db99a3e"
	# 
    DS_EXECUTE_INTENTIONS_SCRIPT = "2f16c4a5-b98e-432c-952a-cb388ba33f2e"
	# 
    DS_INSTALL_REPLICA = "9923a32a-3607-11d2-b9be-0000f87a36b2"
	# 
    DS_QUERY_SELF_QUOTA = "4ecc03fe-ffc0-4947-b630-eb672a8a9dbc"
	# 
    DS_REPLICATION_GET_CHANGES = "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2"
	# 
    DS_REPLICATION_GET_CHANGES_ALL = "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2"
	# 
    DS_REPLICATION_GET_CHANGES_IN_FILTERED_SET = "89e95b76-444d-4c62-991a-0facbeda640c"
	# 
    DS_REPLICATION_MANAGE_TOPOLOGY = "1131f6ac-9c07-11d1-f79f-00c04fc2dcd2"
	# 
    DS_REPLICATION_MONITOR_TOPOLOGY = "f98340fb-7c5b-4cdb-a00b-2ebdfa115a96"
	# 
    DS_REPLICATION_SYNCHRONIZE = "1131f6ab-9c07-11d1-f79f-00c04fc2dcd2"
	# 
    ENABLE_PER_USER_REVERSIBLY_ENCRYPTED_PASSWORD = "05c74c5e-4deb-43b4-bd9f-86664c2a7fd5"
	# 
    GENERATE_RSOP_LOGGING = "b7b1b3de-ab09-4242-9e30-9980e5d322f7"
	# 
    GENERATE_RSOP_PLANNING = "b7b1b3dd-ab09-4242-9e30-9980e5d322f7"
	# 
    MANAGE_OPTIONAL_FEATURES = "7c0e2a7c-a419-48e4-a995-10180aad54dd"
	# 
    MIGRATE_SID_HISTORY = "ba33815a-4f93-4c76-87f3-57574bff8109"
	# 
    MSMQ_OPEN_CONNECTOR = "b4e60130-df3f-11d1-9c86-006008764d0e"
	# 
    MSMQ_PEEK = "06bd3201-df3e-11d1-9c86-006008764d0e"
	# 
    MSMQ_PEEK_COMPUTER_JOURNAL = "4b6e08c3-df3c-11d1-9c86-006008764d0e"
	# 
    MSMQ_PEEK_DEAD_LETTER = "4b6e08c1-df3c-11d1-9c86-006008764d0e"
	# 
    MSMQ_RECEIVE = "06bd3200-df3e-11d1-9c86-006008764d0e"
	# 
    MSMQ_RECEIVE_COMPUTER_JOURNAL = "4b6e08c2-df3c-11d1-9c86-006008764d0e"
	# 
    MSMQ_RECEIVE_DEAD_LETTER = "4b6e08c0-df3c-11d1-9c86-006008764d0e"
	# 
    MSMQ_RECEIVE_JOURNAL = "06bd3203-df3e-11d1-9c86-006008764d0e"
	# 
    MSMQ_SEND = "06bd3202-df3e-11d1-9c86-006008764d0e"
	# 
    OPEN_ADDRESS_BOOK = "a1990816-4298-11d1-ade2-00c04fd8d5cd"
	# 
    READ_ONLY_REPLICATION_SECRET_SYNCHRONIZATION = "1131f6ae-9c07-11d1-f79f-00c04fc2dcd2"
	# 
    REANIMATE_TOMBSTONES = "45ec5156-db7e-47bb-b53f-dbeb2d03c40f"
	# 
    RECALCULATE_HIERARCHY = "0bc1554e-0a99-11d1-adbb-00c04fd8d5cd"
	# 
    RECALCULATE_SECURITY_INHERITANCE = "62dd28a8-7f46-11d2-b9ad-00c04f79f805"
	# 
    RECEIVE_AS = "ab721a56-1e2f-11d0-9819-00aa0040529b"
	# 
    REFRESH_GROUP_CACHE = "9432c620-033c-4db7-8b58-14ef6d0bf477"
	# 
    RELOAD_SSL_CERTIFICATE = "1a60ea8d-58a6-4b20-bcdc-fb71eb8a9ff8"
	# 
    RUN_PROTECT_ADMIN_GROUPS_TASK = "7726b9d5-a4b4-4288-a6b2-dce952e80a7f"
	# 
    SAM_ENUMERATE_ENTIRE_DOMAIN = "91d67418-0135-4acc-8d79-c08e857cfbec"
	# 
    SEND_AS = "ab721a54-1e2f-11d0-9819-00aa0040529b"
	# 
    SEND_TO = "ab721a55-1e2f-11d0-9819-00aa0040529b"
	# 
    UNEXPIRE_PASSWORD = "ccc2dc7d-a6ad-4a7a-8846-c04e3cc53501"
	# 
    UPDATE_PASSWORD_NOT_REQUIRED_BIT = "280f369c-67c7-438e-ae98-1d46f3c6f541"
	# 
    UPDATE_SCHEMA_CACHE = "be2bb760-7f46-11d2-b9ad-00c04f79f805"
	# 
    USER_CHANGE_PASSWORD = "ab721a53-1e2f-11d0-9819-00aa0040529b"
	# 
    USER_FORCE_CHANGE_PASSWORD = "00299570-246d-11d0-a768-00aa006e0529"


## SID 


class SID_IDENTIFIER_AUTHORITY(Enum):
    """
    Source: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/c6ce4275-3d90-4890-ab3a-514745e4637e
    """
    NULL_SID_AUTHORITY = 0x00
    WORLD_SID_AUTHORITY = 0x01
    LOCAL_SID_AUTHORITY = 0x02
    CREATOR_SID_AUTHORITY = 0x03
    NON_UNIQUE_AUTHORITY = 0x04
    SECURITY_NT_AUTHORITY = 0x05
    SECURITY_APP_PACKAGE_AUTHORITY = 0x0f
    SECURITY_MANDATORY_LABEL_AUTHORITY = 0x10
    SECURITY_SCOPED_POLICY_ID_AUTHORITY = 0x11
    SECURITY_AUTHENTICATION_AUTHORITY = 0x12


class SID(object):
    """
    Represents a Security Identifier (SID) in various formats and provides methods for manipulation and conversion between them.

    Attributes:
        revisionLevel (int): The revision level of the SID.
        subAuthorityCount (int): The number of sub-authorities in the SID.
        identifierAuthority (SID_IDENTIFIER_AUTHORITY): The identifier authority value.
        reserved (bytes): Reserved bytes, should always be empty.
        subAuthorities (list): A list of sub-authorities.
        relativeIdentifier (int): The relative identifier.

    Methods:
        load(data): Class method to load a SID from either a string or raw bytes.
        fromStrFormat(data): Class method to create a SID instance from a string representation.
        fromRawBytes(data): Class method to create a SID instance from raw bytes.

    See: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/f992ad60-0fe4-4b87-9fed-beb478836861
    """
    
    bytesize = 0
    
    revisionLevel = 0
    subAuthorityCount = 0
    identifierAuthority = 0
    reserved = b''
    subAuthorities = []
    relativeIdentifier = 0

    wellKnownSIDs =  {
        "S-1-0-0": "Nobody",
        "S-1-1-0": "World",
        "S-1-2-0": "Local",
        "S-1-2-1": "Console Logon",
        "S-1-3-0": "Creator Owner",
        "S-1-3-1": "Creator Group",
        "S-1-3-2": "Creator Owner Server",
        "S-1-3-3": "Creator Owner Group",
        "S-1-3-4": "Owner rights",
        "S-1-5-1": "Dialup DIALUP",
        "S-1-5-2": "NT AUTHORITY\\NETWORK",
        "S-1-5-3": "NT AUTHORITY\\BATCH",
        "S-1-5-4": "NT AUTHORITY\\INTERACTIVE",
        #"S-1-5-5-x-y": "Logon SID identifying logon session. This SID can be queried using whoami.exe /logonid",
        "S-1-5-6": "SERVICE",
        "S-1-5-7": "ANONYMOUS LOGON",
        "S-1-5-8": "PROXY",
        "S-1-5-9": "ENTERPRISE DOMAIN CONTROLLERS",
        "S-1-5-10": "SELF",
        "S-1-5-11": "NT AUTHORITY\\Authenticated Users",
        "S-1-5-12": "NT AUTHORITY\\RESTRICTED",
        "S-1-5-13": "TERMINAL SERVER USER",
        "S-1-5-14": "NT AUTHORITY\\REMOTE INTERACTIVE LOGON",
        "S-1-5-15": "NT AUTHORITY\\This Organization",
        "S-1-5-17": "NT AUTHORITY\\IUSR",
        "S-1-5-18": "NT AUTHORITY\\SYSTEM",
        "S-1-5-19": "NT AUTHORITY\\LOCAL SERVICE",
        "S-1-5-20": "NT AUTHORITY\\NETWORK SERVICE",
        #"S-1-5-21-…": "User accounts (and also domains?)",
        #"S-1-5-21-do-ma-in-500": "(local?) Administrator",
        #"S-1-5-21-do-ma-in-501": "A domain's guest account which allows users that don't have a domain account to log in",
        #"S-1-5-21-do-ma-in-503": "The Default Account (aka Default System Managed Account)",
        #"S-1-5-21-do-ma-in-504": "",
        "S-1-5-32": "The built-in domain, it contains groups that define roles on a local machine. BUILTIN",
        "S-1-5-32-544": "BUILTIN\\Administrators",
        "S-1-5-32-545": "BUILTIN\\Users",
        "S-1-5-32-546": "BUILTIN\\Guests",
        "S-1-5-32-547": "BUILTIN\\Power Users",
        "S-1-5-32-551": "BUILTIN\\Backup Operators",
        "S-1-5-32-552": "BUILTIN\\Replicator",
        "S-1-5-32-554": "BUILTIN\\Pre-Windows 2000 Compatible Access",
        "S-1-5-32-555": "BUILTIN\\Remote Desktop Users",
        "S-1-5-32-558": "BUILTIN\\Performance Monitor Users",
        "S-1-5-32-559": "BUILTIN\\Performance Log Users",
        "S-1-5-32-568": "BUILTIN\\IIS_IUSRS",
        "S-1-5-32-569": "BUILTIN\\Cryptographic Operators",
        "S-1-5-32-573": "BUILTIN\\Event Log Readers",
        "S-1-5-32-578": "BUILTIN\\Hyper-V Administrators",
        "S-1-5-32-579": "BUILTIN\\Access Control Assistance Operators",
        "S-1-5-32-581": "BUILTIN\\System Managed Accounts Group",
        "S-1-5-32-583": "BUILTIN\\Device Owners",
        "S-1-5-64-10": "NTLM Authentication",
        "S-1-5-80": "All services",
        # "S-1-5-80-…": "The SID of a particular service NT SERVICE\\…",
        "S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464": "Trusted installer NT SERVICE\\TrustedInstaller",
        # "S-1-5-94-…": "Windows Remoting Virtual Users",
        "S-1-5-113": "Local account",
        "S-1-5-114": "Local account and member of Administrators group German: NT-AUTORITÄT\\Lokales Konto und Mitglied der Gruppse \"Administratoren\"",
        "S-1-15-2-1": "All applications running in an app package context. APPLICATION PACKAGE AUTHORITY\\ALL APPLICATION PACKAGES",
        # "S-1-15-3-…": "All capability SIDs start with S-1-15-3.",
        # "S-1-16-…": "Mandatory Level See processes: integrity levels",
        "S-1-18-1": "Authentication authority asserted identity"
    }

    @classmethod
    def load(cls, data):
        self = None

        if type(data) == bytes and len(data) == 16:
            return SID.fromRawBytes(data)

        return self
    
    @classmethod
    def fromStrFormat(cls, data: str):
        """
        Creates a SID instance from a string representation.

        This method parses a string representation of a SID and initializes the class attributes based on the parsed values.
        The expected string format is "S-1-5-21-2127521184-1604012920-1887927527-171278", where each part after "S-1-" represents a sub-authority.

        Args:
            data (str): The string representation of a SID.

        Returns:
            SID: An instance of the SID class populated with the parsed data, or None if the string format is invalid.
        """

        matched = re.findall(r'(^S-(\d+)-(\d+))', data, re.IGNORECASE)
        if matched is not None:
            self = cls()

            return self
        else:
            return None

    @classmethod
    def fromRawBytes(cls, data: bytes):
        """
        Creates a SID instance from raw bytes.

        This method parses the raw bytes to extract the SID components according to the SID structure.
        It sets the class attributes based on the extracted values.

        Args:
            data (bytes): The raw bytes representing a SID.

        Returns:
            SID: An instance of the SID class populated with the parsed data.
        """

        self = cls()

        rawData = io.BytesIO(data)

        self.bytesize = 0

        self.revisionLevel = struct.unpack('<B', rawData.read(1))[0]
        self.bytesize += 1

        self.subAuthorityCount = struct.unpack('<B', rawData.read(1))[0]
        self.bytesize += 1

        __value = struct.unpack('>H', rawData.read(2))[0] << 16
        __value += struct.unpack('>H', rawData.read(2))[0] << 8
        __value += struct.unpack('>H', rawData.read(2))[0]

        self.identifierAuthority = SID_IDENTIFIER_AUTHORITY(__value)
        self.bytesize += 6

        self.subAuthorities = []
        for k in range(self.subAuthorityCount-1):
            self.subAuthorities.append(struct.unpack('<I', rawData.read(4))[0])
            self.bytesize += 4
        
        self.relativeIdentifier = struct.unpack('<I', rawData.read(4))[0]
        self.bytesize += 4

        return self
    
    def toRawBytes(self):
        """
        Converts the SID instance into its raw bytes representation.

        This method packs the SID attributes into a sequence of bytes according to the SID structure. It starts with the revision level, followed by the sub-authority count, the identifier authority, each of the sub-authorities, and finally the relative identifier.

        Returns:
            bytes: The raw bytes representation of the SID.
        """

        data = b''
        data += struct.pack("<B", self.revisionLevel)
        data += struct.pack("<B", self.subAuthorityCount)
        data += struct.pack(">H", self.identifierAuthority.value >> 16)
        data += struct.pack(">H", self.identifierAuthority.value >> 8)
        data += struct.pack(">H", self.identifierAuthority.value)
        for __subAuthority in self.subAuthorities:
            data += struct.pack("<I", __subAuthority)
        data += struct.pack("<I", self.relativeIdentifier)
        return data

    def toString(self):
        """
        Converts the SID instance into a string representation.

        This method constructs a string representation of the SID by concatenating the revision level, identifier authority value, sub-authorities, and the relative identifier, separated by hyphens. The string is prefixed with "S-" to denote a SID string.

        Returns:
            str: The string representation of the SID.
        """

        elements = [self.revisionLevel, self.identifierAuthority.value] + self.subAuthorities + [self.relativeIdentifier]

        return "S-%s" % '-'.join([str(e) for e in elements])
    
    def __str__(self):
        """
        Provides a string representation of the SID instance.

        This method returns a string representation of the SID. If the SID is recognized as a well-known SID, it returns the SID string directly. Otherwise, it appends the description of the SID (if available in the `wellKnownSIDs` dictionary) to the SID string.

        Returns:
            str: The string representation of the SID, optionally appended with its description.
        """
        str_repr = self.toString()
        if str_repr not in self.wellKnownSIDs.keys():
            return "<SID '%s'>" % str_repr
        else:
            return "<SID '%s' (%s)>" % (str_repr, self.wellKnownSIDs[str_repr])

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<SID at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        str_repr = self.toString()
        if str_repr not in self.wellKnownSIDs.keys():
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m" % (indent_prompt, str_repr))
        else:
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, str_repr, self.wellKnownSIDs[str_repr]))
        print(''.join(["  │ "]*indent + ["  └─"]))    

# Aliases

SecurityIdentifier = SID

## GUID

class GUIDFormat(Enum):
    """
    N => 32 digits : 00000000000000000000000000000000
    D => 32 digits separated by hyphens : 00000000-0000-0000-0000-000000000000
    B => 32 digits separated by hyphens, enclosed in braces : {00000000-0000-0000-0000-000000000000}
    P => 32 digits separated by hyphens, enclosed in parentheses : (00000000-0000-0000-0000-000000000000)
    X => Four hexadecimal values enclosed in braces, where the fourth value is a subset of eight hexadecimal values that is also enclosed in braces : {0x00000000,0x0000,0x0000,{0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}}
    """
    N = 0
    D = 1
    B = 2
    P = 3
    X = 4


class GUIDImportFormatPattern(Enum):
    """
    N => 32 digits : 00000000000000000000000000000000
    D => 32 digits separated by hyphens : 00000000-0000-0000-0000-000000000000
    B => 32 digits separated by hyphens, enclosed in braces : {00000000-0000-0000-0000-000000000000}
    P => 32 digits separated by hyphens, enclosed in parentheses : (00000000-0000-0000-0000-000000000000)
    X => Four hexadecimal values enclosed in braces, where the fourth value is a subset of eight hexadecimal values that is also enclosed in braces : {0x00000000,0x0000,0x0000,{0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}}
    """
    N = "^([0-9a-f]{8})([0-9a-f]{4})([0-9a-f]{4})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$"
    D = "^([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})$"
    B = "^{([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})}$"
    P = "^\\(([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})\\)$"
    X = "^{0x([0-9a-f]{8}),0x([0-9a-f]{4}),0x([0-9a-f]{4}),{0x([0-9a-f]{2}),0x([0-9a-f]{2}),0x([0-9a-f]{2}),0x([0-9a-f]{2}),0x([0-9a-f]{2}),0x([0-9a-f]{2}),0x([0-9a-f]{2}),0x([0-9a-f]{2})}}$"


class InvalidGUIDFormat(Exception):
    pass


class GUID(object):
    """
    GUID

    See: https://docs.microsoft.com/en-us/dotnet/api/system.GUID?view=net-5.0
    """

    Format: GUIDFormat = None

    def __init__(self, a=None, b=None, c=None, d=None, e=None):
        super(GUID, self).__init__()
        if a is None:
            a = sum([random.randint(0, 0xff) << (8*k) for k in range(4)])
        if b is None:
            b = sum([random.randint(0, 0xff) << (8*k) for k in range(2)])
        if c is None:
            c = sum([random.randint(0, 0xff) << (8*k) for k in range(2)])
        if d is None:
            d = sum([random.randint(0, 0xff) << (8*k) for k in range(2)])
        if e is None:
            e = sum([random.randint(0, 0xff) << (8*k) for k in range(6)])
        self.a, self.b, self.c, self.d, self.e = a, b, c, d, e

    @classmethod
    def load(cls, data):
        self = None

        if type(data) == bytes and len(data) == 16:
            return GUID.fromRawBytes(data)

        elif type(data) == str:
            matched = re.match(GUIDImportFormatPattern.X.value, data, re.IGNORECASE)
            if matched is not None:
                self = cls.fromFormatX(matched.group(0))
                self.Format = GUIDFormat.X
                return self

            matched = re.match(GUIDImportFormatPattern.P.value, data, re.IGNORECASE)
            if matched is not None:
                self = cls.fromFormatP(matched.group(0))
                self.Format = GUIDFormat.P
                return self

            matched = re.match(GUIDImportFormatPattern.D.value, data, re.IGNORECASE)
            if matched is not None:
                self = cls.fromFormatD(matched.group(0))
                self.Format = GUIDFormat.D
                return self

            matched = re.match(GUIDImportFormatPattern.B.value, data, re.IGNORECASE)
            if matched is not None:
                self = cls.fromFormatB(matched.group(0))
                self.Format = GUIDFormat.B
                return self

            matched = re.match(GUIDImportFormatPattern.N.value, data, re.IGNORECASE)
            if matched is not None:
                self = cls.fromFormatN(matched.group(0))
                self.Format = GUIDFormat.N
                return self

        return self

    # Import formats

    @classmethod
    def fromRawBytes(cls, data: bytes):
        if len(data) != 16:
            raise InvalidGUIDFormat("fromRawBytes takes exactly 16 bytes of data in input")
        # 0xffffff
        a = struct.unpack("<L", data[0:4])[0]
        # 0xffff
        b = struct.unpack("<H", data[4:6])[0]
        # 0xffff
        c = struct.unpack("<H", data[6:8])[0]
        # 0xffff
        d = struct.unpack(">H", data[8:10])[0]
        # 0xffffffffffff
        e = binascii.hexlify(data[10:16]).decode("UTF-8").rjust(6, '0')
        e = int(e, 16)
        self = cls(a, b, c, d, e)
        return self

    @classmethod
    def fromFormatN(cls, data):
        # N => 32 digits : 00000000000000000000000000000000
        if not re.match(GUIDImportFormatPattern.N.value, data, re.IGNORECASE):
            raise InvalidGUIDFormat("GUID Format N should be 32 hexadecimal characters separated in five parts.")
        a = int(data[0:8], 16)
        b = int(data[8:12], 16)
        c = int(data[12:16], 16)
        d = int(data[16:20], 16)
        e = int(data[20:32], 16)
        self = cls(a, b, c, d, e)
        return self

    @classmethod
    def fromFormatD(cls, data):
        # D => 32 digits separated by hyphens :
        # 00000000-0000-0000-0000-000000000000
        if not re.match(GUIDImportFormatPattern.D.value, data, re.IGNORECASE):
            raise InvalidGUIDFormat("GUID Format D should be 32 hexadecimal characters separated in five parts.")
        a, b, c, d, e = map(lambda x: int(x, 16), data.split("-"))
        self = cls(a, b, c, d, e)
        return self

    @classmethod
    def fromFormatB(cls, data):
        # B => 32 digits separated by hyphens, enclosed in braces :
        # {00000000-0000-0000-0000-000000000000}
        if not re.match(GUIDImportFormatPattern.B.value, data, re.IGNORECASE):
            raise InvalidGUIDFormat("GUID Format B should be 32 hexadecimal characters separated in five parts enclosed in braces.")
        a, b, c, d, e = map(lambda x: int(x, 16), data[1:-1].split("-"))
        self = cls(a, b, c, d, e)
        return self

    @classmethod
    def fromFormatP(cls, data):
        # P => 32 digits separated by hyphens, enclosed in parentheses :
        # (00000000-0000-0000-0000-000000000000)
        if not re.match(GUIDImportFormatPattern.P.value, data, re.IGNORECASE):
            raise InvalidGUIDFormat("GUID Format P should be 32 hexadecimal characters separated in five parts enclosed in parentheses.")
        a, b, c, d, e = map(lambda x: int(x, 16), data[1:-1].split("-"))
        self = cls(a, b, c, d, e)
        return self

    @classmethod
    def fromFormatX(cls, data):
        # X => Four hexadecimal values enclosed in braces, where the fourth value is a subset of
        # eight hexadecimal values that is also enclosed in braces :
        # {0x00000000,0x0000,0x0000,{0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}}
        if not re.match(GUIDImportFormatPattern.X.value, data, re.IGNORECASE):
            raise InvalidGUIDFormat("GUID Format X should be in this format {0x00000000,0x0000,0x0000,{0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}}.")
        hex_a, hex_b, hex_c, rest = data[1:-1].split(',', 3)
        rest = rest[1:-1].split(',')
        a = int(hex_a, 16)
        b = int(hex_b, 16)
        c = int(hex_c, 16)
        d = int(rest[0], 16) * 0x100 + int(rest[1], 16)
        e = int(rest[2], 16) * (0x1 << (8 * 5))
        e += int(rest[3], 16) * (0x1 << (8 * 4))
        e += int(rest[4], 16) * (0x1 << (8 * 3))
        e += int(rest[5], 16) * (0x1 << (8 * 2))
        e += int(rest[6], 16) * (0x1 << 8)
        e += int(rest[7], 16)
        self = cls(a, b, c, d, e)
        return self

    # Export formats

    def toRawBytes(self):
        data = b''
        data += struct.pack("<L", self.a)
        data += struct.pack("<H", self.b)
        data += struct.pack("<H", self.c)
        data += struct.pack(">H", self.d)
        data += binascii.unhexlify(hex(self.e)[2:].rjust(12, '0'))
        return data

    def toFormatN(self) -> str:
        # N => 32 digits :
        # 00000000000000000000000000000000
        hex_a = hex(self.a)[2:].rjust(8, '0')
        hex_b = hex(self.b)[2:].rjust(4, '0')
        hex_c = hex(self.c)[2:].rjust(4, '0')
        hex_d = hex(self.d)[2:].rjust(4, '0')
        hex_e = hex(self.e)[2:].rjust(12, '0')
        return "%s%s%s%s%s" % (hex_a, hex_b, hex_c, hex_d, hex_e)

    def toFormatD(self) -> str:
        # D => 32 digits separated by hyphens :
        # 00000000-0000-0000-0000-000000000000
        hex_a = hex(self.a)[2:].rjust(8, '0')
        hex_b = hex(self.b)[2:].rjust(4, '0')
        hex_c = hex(self.c)[2:].rjust(4, '0')
        hex_d = hex(self.d)[2:].rjust(4, '0')
        hex_e = hex(self.e)[2:].rjust(12, '0')
        return "%s-%s-%s-%s-%s" % (hex_a, hex_b, hex_c, hex_d, hex_e)

    def toFormatB(self) -> str:
        # B => 32 digits separated by hyphens, enclosed in braces :
        # {00000000-0000-0000-0000-000000000000}
        hex_a = hex(self.a)[2:].rjust(8, '0')
        hex_b = hex(self.b)[2:].rjust(4, '0')
        hex_c = hex(self.c)[2:].rjust(4, '0')
        hex_d = hex(self.d)[2:].rjust(4, '0')
        hex_e = hex(self.e)[2:].rjust(12, '0')
        return "{%s-%s-%s-%s-%s}" % (hex_a, hex_b, hex_c, hex_d, hex_e)

    def toFormatP(self) -> str:
        # P => 32 digits separated by hyphens, enclosed in parentheses :
        # (00000000-0000-0000-0000-000000000000)
        hex_a = hex(self.a)[2:].rjust(8, '0')
        hex_b = hex(self.b)[2:].rjust(4, '0')
        hex_c = hex(self.c)[2:].rjust(4, '0')
        hex_d = hex(self.d)[2:].rjust(4, '0')
        hex_e = hex(self.e)[2:].rjust(12, '0')
        return "(%s-%s-%s-%s-%s)" % (hex_a, hex_b, hex_c, hex_d, hex_e)

    def toFormatX(self) -> str:
        # X => Four hexadecimal values enclosed in braces, where the fourth value is a subset of
        # eight hexadecimal values that is also enclosed in braces :
        # {0x00000000,0x0000,0x0000,{0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}}
        hex_a = hex(self.a)[2:].rjust(8, '0')
        hex_b = hex(self.b)[2:].rjust(4, '0')
        hex_c = hex(self.c)[2:].rjust(4, '0')
        hex_d = hex(self.d)[2:].rjust(4, '0')
        hex_d1, hex_d2 = hex_d[:2], hex_d[2:4]
        hex_e = hex(self.e)[2:].rjust(12, '0')
        hex_e1, hex_e2, hex_e3, hex_e4, hex_e5, hex_e6 = hex_e[:2], hex_e[2:4], hex_e[4:6], hex_e[6:8], hex_e[8:10], hex_e[10:12]
        return "{0x%s,0x%s,0x%s,{0x%s,0x%s,0x%s,0x%s,0x%s,0x%s,0x%s,0x%s}}" % (hex_a, hex_b, hex_c, hex_d1, hex_d2, hex_e1, hex_e2, hex_e3, hex_e4, hex_e5, hex_e6)

    def __repr__(self):
        return "<GUID %s>" % self.toFormatB()


## 

class OwnerSID(object):
    """
    Represents an Owner Security Identifier (SID) in a security descriptor.

    Attributes:
        verbose (bool): If True, enables verbose output for debugging.
        value (bytes): The raw bytes representing the SID.
        bytesize (int): The size in bytes of the SID.
        sid (SID): An instance of the SID class representing the parsed SID.

    Methods:
        parse(value=None): Parses the raw bytes to extract the SID. Optionally takes a new value to parse.
        describe(offset=0, indent=0): Prints a formatted description of the OwnerSID, including its offset, size, and SID value.
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        self.sid = SID.fromRawBytes(self.value)
        self.bytesize = self.sid.bytesize

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<OwnerSID at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        str_repr = self.sid.toString()
        if str_repr not in self.sid.wellKnownSIDs.keys():
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m" % (indent_prompt, str_repr))
        else:
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, str_repr, self.sid.wellKnownSIDs[str_repr]))
        print(''.join(["  │ "]*indent + ["  └─"]))


class GroupSID(object):
    """
    Represents a Group Security Identifier (SID) in a security descriptor.

    Attributes:
        verbose (bool): If True, enables verbose output for debugging.
        value (bytes): The raw bytes representing the SID.
        bytesize (int): The size in bytes of the SID.
        sid (SID): An instance of the SID class representing the parsed SID.

    Methods:
        parse(value=None): Parses the raw bytes to extract the SID. Optionally takes a new value to parse.
        describe(offset=0, indent=0): Prints a formatted description of the GroupSID, including its offset, size, and SID value.
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        self.sid = SID.fromRawBytes(self.value)
        self.bytesize = self.sid.bytesize

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<GroupSID at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        str_repr = self.sid.toString()
        if str_repr not in self.sid.wellKnownSIDs.keys():
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m" % (indent_prompt, str_repr))
        else:
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, str_repr, self.sid.wellKnownSIDs[str_repr]))
        print(''.join(["  │ "]*indent + ["  └─"]))


class ACESID(object):
    """
    Represents an Access Control Entry's Security Identifier (SID) in a Discretionary Access Control List (DACL) or System Access Control List (SACL).

    Attributes:
        verbose (bool): If True, enables verbose output for debugging.
        value (bytes): The raw bytes representing the SID.
        bytesize (int): The size in bytes of the SID.
        sid (SID): An instance of the SID class representing the parsed SID.

    Methods:
        parse(value=None): Parses the raw bytes to extract the SID. Optionally takes a new value to parse.
        describe(offset=0, indent=0): Prints a formatted description of the ACESID, including its offset, size, and SID value.
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        self.sid = SID.fromRawBytes(self.value)
        self.bytesize = self.sid.bytesize

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<ACESID at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        str_repr = self.sid.toString()
        if str_repr not in self.sid.wellKnownSIDs.keys():
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m" % (indent_prompt, str_repr))
        else:
            print("%s  │ \x1b[93mSID\x1b[0m : \x1b[96m%s\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, str_repr, self.sid.wellKnownSIDs[str_repr]))
        print(''.join(["  │ "]*indent + ["  └─"]))  

## ACE

class AccessControlObjectTypeFlags(IntFlag):
    """
    A set of bit flags that indicate whether the ObjectType and InheritedObjectType members are present. This parameter can be one or more of the following values.
    
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-access_allowed_object_ace
    """
    NONE = 0x00000000 # Neither ObjectType nor InheritedObjectType are valid.
    ACE_OBJECT_TYPE_PRESENT = 0x00000001 # ObjectType is valid.
    ACE_INHERITED_OBJECT_TYPE_PRESENT = 0x00000002 # InheritedObjectType is valid. If this value is not specified, all types of child objects can inherit the ACE.


class AccessControlObjectType(object):
    """
    Represents an Access Control Object Type, which is a component of an Access Control Entry (ACE) that
    specifies the type of object or property to which an access control applies. This class parses and
    encapsulates the object type information from a binary representation into a more accessible form.

    Attributes:
        verbose (bool): If set to True, provides detailed parsing information.
        value (bytes): The binary representation of the Access Control Object Type.
        bytesize (int): The size in bytes of the Access Control Object Type.
        guid (GUID): The globally unique identifier (GUID) associated with the object type.
        flags (int): Flags that provide additional information about the object type.

    Methods:
        parse(value=None): Parses the binary representation to extract the GUID and flags.
        describe(offset=0, indent=0): Prints a formatted description of the Access Control Object Type.
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        self.ObjectTypeGuid = None
        self.InheritedObjectTypeGuid = None
        self.flags = 0
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        rawData = io.BytesIO(self.value)

        self.bytesize = 4
        self.flags = AccessControlObjectTypeFlags(struct.unpack("<I", rawData.read(4))[0])

        if (self.flags & AccessControlObjectTypeFlags.ACE_OBJECT_TYPE_PRESENT) and (self.flags & AccessControlObjectTypeFlags.ACE_INHERITED_OBJECT_TYPE_PRESENT):
            self.bytesize += 16
            self.ObjectTypeGuid = GUID.fromRawBytes(rawData.read(16))
            self.bytesize += 16
            self.InheritedObjectTypeGuid = GUID.fromRawBytes(rawData.read(16))

        elif (self.flags & AccessControlObjectTypeFlags.ACE_OBJECT_TYPE_PRESENT):
            self.bytesize += 16
            self.ObjectTypeGuid = GUID.fromRawBytes(rawData.read(16))
        
        elif (self.flags & AccessControlObjectTypeFlags.ACE_INHERITED_OBJECT_TYPE_PRESENT):
            self.bytesize += 16
            self.InheritedObjectTypeGuid = GUID.fromRawBytes(rawData.read(16))

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<AccessControlObjectType at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        print("%s  │ \x1b[93mFlags\x1b[0m : \x1b[96m0x%08x\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, self.flags.value, self.flags.name))
        
        if self.ObjectTypeGuid is not None:
            guid_format_d = self.ObjectTypeGuid.toFormatD()
            if guid_format_d in [er.value for er in ExtendedRights]:
                print("%s  │ \x1b[93mObjectTypeGuid\x1b[0m  : \x1b[96m%s\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, guid_format_d, ExtendedRights(guid_format_d).name))
            else:
                print("%s  │ \x1b[93mObjectTypeGuid\x1b[0m  : \x1b[96m%s\x1b[0m" % (indent_prompt, guid_format_d))
        
        if self.InheritedObjectTypeGuid is not None:
            guid_format_d = self.InheritedObjectTypeGuid.toFormatD()
            if guid_format_d in [er.value for er in ExtendedRights]:
                print("%s  │ \x1b[93mInheritedObjectTypeGuid\x1b[0m  : \x1b[96m%s\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, guid_format_d, ExtendedRights(guid_format_d).name))
            else:
                print("%s  │ \x1b[93mInheritedObjectTypeGuid\x1b[0m  : \x1b[96m%s\x1b[0m" % (indent_prompt, guid_format_d))
        
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def keys(self):
        return self.__data.keys()


class AccessMaskFlags(IntFlag):
    """
    AccessMaskFlags: Enum class that defines constants for access mask flags.

    This class defines constants for various access mask flags as specified in the Microsoft documentation. These flags represent permissions or rights that can be granted or denied for security principals in access control entries (ACEs) of an access control list (ACL).

    The flags include permissions for creating or deleting child objects, listing contents, reading or writing properties, deleting a tree of objects, and controlling access. Additionally, it includes generic rights like GENERIC_ALL, GENERIC_EXECUTE, GENERIC_WRITE, and GENERIC_READ.

    The values for these flags are derived from the following Microsoft documentation sources:
    - https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/7a53f60e-e730-4dfe-bbe9-b21b62eb790b
    - https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/990fb975-ab31-4bc1-8b75-5da132cd4584
    - https://learn.microsoft.com/en-us/windows/win32/api/iads/ne-iads-ads_rights_enum

    Attributes:
        DS_CREATE_CHILD (int): Permission to create child objects.
        DS_DELETE_CHILD (int): Permission to delete child objects.
        DS_LIST_CONTENTS (int): Permission to list contents.
        DS_WRITE_PROPERTY_EXTENDED (int): Permission to write properties (extended).
        DS_READ_PROPERTY (int): Permission to read properties.
        DS_WRITE_PROPERTY (int): Permission to write properties.
        DS_DELETE_TREE (int): Permission to delete a tree of objects.
        DS_LIST_OBJECT (int): Permission to list objects.
        DS_CONTROL_ACCESS (int): Permission for access control.
        DELETE (int): Permission to delete.
        READ_CONTROL (int): Permission to read security descriptor.
        WRITE_DAC (int): Permission to modify discretionary access control list (DACL).
        WRITE_OWNER (int): Permission to change the owner.
        GENERIC_ALL (int): Generic all permissions.
        GENERIC_EXECUTE (int): Generic execute permissions.
        GENERIC_WRITE (int): Generic write permissions.
        GENERIC_READ (int): Generic read permissions.
    """

    DS_CREATE_CHILD = 0x00000001
    DS_DELETE_CHILD = 0x00000002
    DS_LIST_CONTENTS = 0x00000004
    DS_WRITE_PROPERTY_EXTENDED = 0x00000008
    DS_READ_PROPERTY = 0x00000010
    DS_WRITE_PROPERTY = 0x00000020
    DS_DELETE_TREE = 0x00000040
    DS_LIST_OBJECT = 0x00000080
    DS_CONTROL_ACCESS = 0x00000100
    DELETE = 0x00010000
    READ_CONTROL = 0x00020000
    WRITE_DAC = 0x00040000
    WRITE_OWNER = 0x00080000
    # Generic rights
    GENERIC_ALL = 0x10000000
    GENERIC_EXECUTE = 0x20000000
    GENERIC_WRITE = 0x40000000
    GENERIC_READ = 0x80000000


class AccessControlMask(object):
    """
    This class represents the Access Control Mask, which is a set of bit flags that define access permissions to an object. These permissions can include the ability to read, write, execute, or delete an object, among others. The Access Control Mask is a crucial component of the security descriptor that defines the security of an object.

    The Access Control Mask is used in conjunction with Access Control Entries (ACEs) within an Access Control List (ACL) to define the security and access permissions for an object. Each ACE contains an Access Control Mask that specifies the permissions granted or denied by that ACE.

    Attributes:
        verbose (bool): If True, enables verbose output for debugging purposes.
        value (bytes): The raw bytes representing the Access Control Mask.
        bytesize (int): The size in bytes of the Access Control Mask.
        AccessMask (int): The integer value of the Access Control Mask, parsed from the raw bytes.
        __data (dict): A dictionary holding the parsed AccessMask and any flags associated with it.

    Methods:
        parse(value=None): Parses the raw bytes to extract the Access Control Mask. Optionally takes a new value to parse.
        describe(offset=0, indent=0): Prints a formatted description of the Access Control Mask, including its value and any flags associated with it.

    Source:
        https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/20233ed8-a6c6-4097-aafa-dd545ed24428
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        self.bytesize = 4
        self.__data = {"AccessMask": 0}
        self.AccessMask = 0
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        rawData = io.BytesIO(self.value)

        self.__data = {"AccessMask": 0, "AccessMaskFlags":[]}

        self.__data["AccessMask"] = AccessMaskFlags(struct.unpack('<I', rawData.read(4))[0])
        self.AccessMask = self.__data["AccessMask"]

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<AccessControlMask at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        print("%s  │ \x1b[93mAccessMask\x1b[0m : \x1b[96m0x%08x\x1b[0m (\x1b[94m%s\x1b[0m)" % (
                indent_prompt,
                self.__data["AccessMask"].value,
                self.__data["AccessMask"].name
            )
        )
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def keys(self):
        return self.__data.keys()


class AccessControlEntry_Flags(IntFlag):
    OBJECT_INHERIT_ACE = 0x01  # Noncontainer child objects inherit the ACE as an effective ACE.
    CONTAINER_INHERIT_ACE = 0x02  # Child objects that are containers, such as directories, inherit the ACE as an effective ACE. The inherited ACE is inheritable unless the NO_PROPAGATE_INHERIT_ACE bit flag is also set.
    NO_PROPAGATE_INHERIT_ACE = 0x04  # If the ACE is inherited by a child object, the system clears the OBJECT_INHERIT_ACE and CONTAINER_INHERIT_ACE flags in the inherited ACE. This prevents the ACE from being inherited by subsequent generations of objects.
    INHERIT_ONLY_ACE = 0x08  # Indicates an inherit-only ACE, which does not control access to the object to which it is attached. If this flag is not set, the ACE is an effective ACE that controls access to the object to which it is attached.
    INHERITED_ACE = 0x10  # Used to indicate that the ACE was inherited. See section 2.5.3.5 for processing rules for setting this flag.
    SUCCESSFUL_ACCESS_ACE_FLAG = 0x40  # Used with system-audit ACEs in a system access control list (SACL) to generate audit messages for successful access attempts.
    FAILED_ACCESS_ACE_FLAG = 0x80  # Used with system-audit ACEs in a system access control list (SACL) to generate audit messages for failed access attempts.


class AccessControlEntry_Type(Enum):
    ACCESS_ALLOWED_ACE_TYPE = 0x00  # Access-allowed ACE that uses the ACCESS_ALLOWED_ACE (section 2.4.4.2) structure.
    ACCESS_DENIED_ACE_TYPE = 0x01  # Access-denied ACE that uses the ACCESS_DENIED_ACE (section 2.4.4.4) structure.
    SYSTEM_AUDIT_ACE_TYPE = 0x02  # System-audit ACE that uses the SYSTEM_AUDIT_ACE (section 2.4.4.10) structure.
    SYSTEM_ALARM_ACE_TYPE = 0x03  # Reserved for future use.
    ACCESS_ALLOWED_COMPOUND_ACE_TYPE = 0x04  # Reserved for future use.
    ACCESS_ALLOWED_OBJECT_ACE_TYPE = 0x05  # Object-specific access-allowed ACE that uses the ACCESS_ALLOWED_OBJECT_ACE (section 2.4.4.3) structure.
    ACCESS_DENIED_OBJECT_ACE_TYPE = 0x06  # Object-specific access-denied ACE that uses the ACCESS_DENIED_OBJECT_ACE (section 2.4.4.5) structure.
    SYSTEM_AUDIT_OBJECT_ACE_TYPE = 0x07  # Object-specific system-audit ACE that uses the SYSTEM_AUDIT_OBJECT_ACE (section 2.4.4.11) structure.
    SYSTEM_ALARM_OBJECT_ACE_TYPE = 0x08  # Reserved for future use.
    ACCESS_ALLOWED_CALLBACK_ACE_TYPE = 0x09  # Access-allowed callback ACE that uses the ACCESS_ALLOWED_CALLBACK_ACE (section 2.4.4.6) structure.
    ACCESS_DENIED_CALLBACK_ACE_TYPE = 0x0A  # Access-denied callback ACE that uses the ACCESS_DENIED_CALLBACK_ACE (section 2.4.4.7) structure.
    ACCESS_ALLOWED_CALLBACK_OBJECT_ACE_TYPE = 0x0B  # Object-specific access-allowed callback ACE that uses the ACCESS_ALLOWED_CALLBACK_OBJECT_ACE (section 2.4.4.8) structure.
    ACCESS_DENIED_CALLBACK_OBJECT_ACE_TYPE = 0x0C  # Object-specific access-denied callback ACE that uses the ACCESS_DENIED_CALLBACK_OBJECT_ACE (section 2.4.4.9) structure.
    SYSTEM_AUDIT_CALLBACK_ACE_TYPE = 0x0D  # System-audit callback ACE that uses the SYSTEM_AUDIT_CALLBACK_ACE (section 2.4.4.12) structure.
    SYSTEM_ALARM_CALLBACK_ACE_TYPE = 0x0E  # Reserved for future use.
    SYSTEM_AUDIT_CALLBACK_OBJECT_ACE_TYPE = 0x0F  # Object-specific system-audit callback ACE that uses the SYSTEM_AUDIT_CALLBACK_OBJECT_ACE (section 2.4.4.14) structure.
    SYSTEM_ALARM_CALLBACK_OBJECT_ACE_TYPE = 0x10  # Reserved for future use.
    SYSTEM_MANDATORY_LABEL_ACE_TYPE = 0x11  # Mandatory label ACE that uses the SYSTEM_MANDATORY_LABEL_ACE (section 2.4.4.13) structure.
    SYSTEM_RESOURCE_ATTRIBUTE_ACE_TYPE = 0x12  # Resource attribute ACE that uses the SYSTEM_RESOURCE_ATTRIBUTE_ACE (section 2.4.4.15).
    SYSTEM_SCOPED_POLICY_ID_ACE_TYPE = 0x13  # A central policy ID ACE that uses the SYSTEM_SCOPED_POLICY_ID_ACE (section 2.4.4.16).


class AccessControlEntry_Header(object):
    """
    Initializes an AccessControlEntry_Header object with the given binary data and optional verbosity flag.

    The AccessControlEntry_Header object represents the header of an Access Control Entry (ACE) in a security descriptor. 
    It contains information about the type of ACE, its flags, and its size. This information is crucial for interpreting 
    the ACE and applying the appropriate access control based on it.

    Parameters:
    - value (bytes): The binary data representing the ACE header.
    - verbose (bool, optional): A flag indicating whether to print detailed parsing information. Defaults to False.

    Attributes:
    - verbose (bool): Indicates whether detailed parsing information is printed.
    - value (bytes): The binary data representing the ACE header.
    - bytesize (int): The size of the ACE header in bytes.
    - __data (dict): A dictionary holding the parsed ACE header fields, including AceType, AceFlags, and AceSize.
    - AceType (AccessControlEntry_Type): The type of the ACE, indicating the action (e.g., allow or deny) and the object it applies to.
    - AceFlags (AccessControlEntry_Flags): Flags providing additional information about the ACE, such as inheritance rules.
    - AceSize (int): The size of the ACE, including the header and the specific data associated with the ACE type.

    Methods:
    - parse(self, value=None): Parses the binary data to populate the ACE header fields. If 'value' is provided, it updates the 'value' attribute before parsing.
    - describe(self, offset=0, indent=0): Prints a formatted description of the ACE header, including its type, flags, and size. 'offset' and 'indent' parameters allow for formatted output within larger structures.

    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/20233ed8-a6c6-4097-aafa-dd545ed24428
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-ace_header
    """
    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        self.bytesize = 4
        self.__data = {
            "AceType": 0,
            "AceFlags": 0,
            "AceSize": 0
        }
        self.AceType = 0
        self.AceFlags = 0
        self.AceSize = 0
        #
        self.parse()
    
    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        rawData = io.BytesIO(self.value)

        self.__data = {
            "AceType": 0,
            "AceFlags": 0,
            "AceSize": 0
        }
        self.AceType = 0
        self.AceFlags = 0
        self.AceSize = 0

        self.bytesize = 0

        # Parsing header
        
        self.__data["AceType"] = AccessControlEntry_Type(struct.unpack('<B', rawData.read(1))[0])
        self.AceType = self.__data["AceType"]
        self.bytesize += 1

        self.__data["AceFlags"] = AccessControlEntry_Flags(struct.unpack('<B', rawData.read(1))[0])
        self.AceFlags = self.__data["AceFlags"]
        self.bytesize += 1

        self.__data["AceSize"] = struct.unpack('<H', rawData.read(2))[0]
        self.AceSize = int(self.__data["AceSize"])
        self.bytesize += 2    

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<AccessControlEntry_Header at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        print("%s  │ \x1b[93mAceType\x1b[0m  : \x1b[96m0x%02x\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, self.__data["AceType"].value, self.__data["AceType"].name))
        print("%s  │ \x1b[93mAceFlags\x1b[0m : \x1b[96m0x%02x\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, self.__data["AceFlags"].value, self.__data["AceFlags"].name))
        print("%s  │ \x1b[93mAceSize\x1b[0m  : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["AceSize"]))
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value


class AccessControlEntry(object):
    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        self.header = None
        self.mask = None
        self.object_type = None
        self.ace_sid = None
        #
        self.parse()

    def parse(self):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))
        
        # Parsing header
        self.header = AccessControlEntry_Header(value=self.value, verbose=self.verbose)

        # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/72e7c7ea-bc02-4c74-a619-818a16bf6adb

        self.value = self.value[self.header.bytesize:]
        self.bytesize = self.header.bytesize

        # Parsing Mask
        self.mask = AccessControlMask(value=self.value, verbose=self.verbose)
        self.value = self.value[self.mask.bytesize:]
        self.bytesize += self.mask.bytesize

        # This is an extended structure
        flags_implying_extended = [
            AccessControlEntry_Type.ACCESS_ALLOWED_OBJECT_ACE_TYPE,
            AccessControlEntry_Type.ACCESS_DENIED_OBJECT_ACE_TYPE,
            AccessControlEntry_Type.SYSTEM_AUDIT_OBJECT_ACE_TYPE,
            AccessControlEntry_Type.SYSTEM_ALARM_OBJECT_ACE_TYPE
        ]
        if any([(f.value & self.header.AceType.value) for f in flags_implying_extended]):
            self.object_type = AccessControlObjectType(value=self.value, verbose=self.verbose)
            self.value = self.value[self.object_type.bytesize:]
            self.bytesize += self.object_type.bytesize

        self.ace_sid = ACESID(value=self.value, verbose=self.verbose)
        self.value = self.value[self.ace_sid.bytesize:]
        self.bytesize += self.ace_sid.bytesize

        if self.verbose:
            self.describe()

    def describe(self, ace_number=0, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<AccessControlEntry #%d at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, ace_number, offset, self.bytesize))
        self.header.describe(offset=offset, indent=(indent + 1))
        offset += self.header.bytesize
        
        self.mask.describe(offset=offset, indent=(indent + 1))
        offset += self.mask.bytesize
                
        if self.object_type is not None:
            self.object_type.describe(offset=offset, indent=(indent + 1))
        
        if self.ace_sid is not None:
            self.ace_sid.describe(offset=offset, indent=(indent + 1))

        print(''.join(["  │ "]*indent + ["  └─"]))

## ACL

class AccessControlList_Revision(Enum):
    ACL_REVISION = 0x02 
    ACL_REVISION_DS = 0x04

## SACL

class SystemAccessControlList_Header(object):
    """
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/20233ed8-a6c6-4097-aafa-dd545ed24428
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-acl
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        self.bytesize = 8
        #
        self.Revision = 0
        self.Sbz1 = 0
        self.AclSize = 0
        self.AceCount = 0
        self.Sbz2 = 0
        #
        self.__data = {
            "Revision": 0,
            "Sbz1": 0,
            "AclSize": 0,
            "AceCount": 0,
            "Sbz2": 0
        }
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))
    
        if value is not None:
            self.value = value

        rawData = io.BytesIO(self.value)

        self.__data = {"Revision": 0, "Sbz1": 0, "AclSize": 0, "AceCount": 0, "Sbz2": 0}

        # Parsing header
        self.__data["Revision"] = AccessControlList_Revision(struct.unpack('<B', rawData.read(1))[0])
        self.Revision = self.__data["Revision"] 

        self.__data["Sbz1"] = struct.unpack('<B', rawData.read(1))[0]
        self.Sbz1 = self.__data["Sbz1"] 

        self.__data["AclSize"] = struct.unpack('<H', rawData.read(2))[0]
        self.AclSize = self.__data["AclSize"] 

        self.__data["AceCount"] = struct.unpack('<H', rawData.read(2))[0]
        self.AceCount = self.__data["AceCount"] 

        self.__data["Sbz2"] = struct.unpack('<H', rawData.read(2))[0]
        self.Sbz2 = self.__data["Sbz2"] 

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<SystemAccessControlList_Header at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        print("%s  │ \x1b[93mRevision\x1b[0m : \x1b[96m0x%02x\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, self.Revision.value, self.Revision.name))
        print("%s  │ \x1b[93mSbz1\x1b[0m     : \x1b[96m0x%02x\x1b[0m" % (indent_prompt, self.__data["Sbz1"]))
        print("%s  │ \x1b[93mAclSize\x1b[0m  : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["AclSize"]))
        print("%s  │ \x1b[93mAceCount\x1b[0m : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["AceCount"]))
        print("%s  │ \x1b[93mSbz2\x1b[0m     : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["Sbz2"]))
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def keys(self):
        return self.__data.keys()


class SystemAccessControlList(object):
    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        #
        self.header = None
        self.entries = []
        #
        self.parse()

    def parse(self):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))
    
        self.header = SystemAccessControlList_Header(value=self.value)
        self.bytesize += self.header.bytesize
        self.value = self.value[self.header.bytesize:]

        # Parsing ACE entries
        self.entries = []
        for k in range(self.header["AceCount"]):
            ace = AccessControlEntry(value=self.value)
            self.entries.append(ace)

            self.bytesize += ace.bytesize
            self.value = self.value[(ace.bytesize):]

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<SystemAccessControlList at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        self.header.describe(offset=offset, indent=(indent + 1))
        offset += self.header.bytesize
        ace_number = 0
        for ace in self.entries:
            ace_number += 1
            ace.describe(ace_number=ace_number, offset=offset, indent=(indent + 1))
            offset += ace.bytesize
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __iter__(self):
        yield from self.entries

    def __len__(self):
        return len(self.entries)

## DACL

class DiscretionaryAccessControlList_Header(object):
    """
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/20233ed8-a6c6-4097-aafa-dd545ed24428
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-acl
    """

    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        self.bytesize = 8
        #
        self.Revision = 0
        self.Sbz1 = 0
        self.AclSize = 0
        self.AceCount = 0
        self.Sbz2 = 0
        #
        self.__data = {
            "Revision": 0,
            "Sbz1": 0,
            "AclSize": 0,
            "AceCount": 0,
            "Sbz2": 0
        }
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))

        if value is not None:
            self.value = value

        rawData = io.BytesIO(self.value)

        self.__data = {"Revision": 0, "Sbz1": 0, "AclSize": 0, "AceCount": 0, "Sbz2": 0}

        # Parsing header
        self.__data["Revision"] = AccessControlList_Revision(struct.unpack('<B', rawData.read(1))[0])
        self.Revision = self.__data["Revision"] 

        self.__data["Sbz1"] = struct.unpack('<B', rawData.read(1))[0]
        self.Sbz1 = self.__data["Sbz1"] 

        self.__data["AclSize"] = struct.unpack('<H', rawData.read(2))[0]
        self.AclSize = self.__data["AclSize"] 

        self.__data["AceCount"] = struct.unpack('<H', rawData.read(2))[0]
        self.AceCount = self.__data["AceCount"] 

        self.__data["Sbz2"] = struct.unpack('<H', rawData.read(2))[0]
        self.Sbz2 = self.__data["Sbz2"] 

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<DiscretionaryAccessControlList_Header at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        print("%s  │ \x1b[93mRevision\x1b[0m : \x1b[96m0x%02x\x1b[0m (\x1b[94m%s\x1b[0m)" % (indent_prompt, self.Revision.value, self.Revision.name))
        print("%s  │ \x1b[93mSbz1\x1b[0m     : \x1b[96m0x%02x\x1b[0m" % (indent_prompt, self.__data["Sbz1"]))
        print("%s  │ \x1b[93mAclSize\x1b[0m  : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["AclSize"]))
        print("%s  │ \x1b[93mAceCount\x1b[0m : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["AceCount"]))
        print("%s  │ \x1b[93mSbz2\x1b[0m     : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["Sbz2"]))
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def keys(self):
        return self.__data.keys()


class DiscretionaryAccessControlList(object):
    def __init__(self, value, verbose=False):
        self.verbose = verbose
        self.value = value
        #
        self.bytesize = 0
        #
        self.header = None
        self.entries = []
        #
        self.parse()

    def parse(self):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))
        
        self.header = DiscretionaryAccessControlList_Header(value=self.value[:8], verbose=self.verbose)
        self.bytesize += self.header.bytesize
        self.value = self.value[self.header.bytesize:]

        # Parsing ACE entries
        self.entries = []
        for k in range(self.header["AceCount"]):
            ace = AccessControlEntry(value=self.value, verbose=self.verbose)
            self.entries.append(ace)

            self.bytesize += ace.bytesize
            self.value = self.value[(ace.bytesize):]

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<DiscretionaryAccessControlList at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        self.header.describe(offset=offset, indent=(indent + 1))
        offset += self.header.bytesize
        ace_number = 0
        for ace in self.entries:
            ace_number += 1
            ace.describe(ace_number=ace_number, offset=offset, indent=(indent + 1))
            offset += ace.bytesize
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __iter__(self):
        yield from self.entries

    def __len__(self):
        return len(self.entries)


class NTSecurityDescriptor_Header(object):
    def __init__(self, value, verbose=False):
        self.bytesize = 20
        self.value = value
        self.__data = {
            "Revision": 0,
            "Sbz1": 0,
            "Control": 0,
            "OffsetOwner": 0,
            "OffsetGroup": 0,
            "OffsetSacl": 0,
            "OffsetDacl": 0
        }
        self.Revision = 0
        self.Sbz1 = 0
        self.Control = 0
        self.OffsetOwner = 0
        self.OffsetGroup = 0
        self.OffsetSacl = 0
        self.sacl = None
        self.OffsetDacl = 0
        self.dacl = None
        self.verbose = verbose
        #
        self.parse()

    def parse(self, value=None):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value[:self.bytesize])))

        if value is not None:
            self.value = value

        rawData = io.BytesIO(self.value)

        self.__data = {"Revision": 0, "Sbz1": 0, "Control": 0, "OffsetOwner": 0, "OffsetGroup": 0, "OffsetSacl": 0, "OffsetDacl": 0}

        # Parsing header
        self.__data["Revision"] = struct.unpack('<B', rawData.read(1))[0]
        self.Revision = self.__data["Revision"]
        
        self.__data["Sbz1"] = struct.unpack('<B', rawData.read(1))[0]
        self.Sbz1 = self.__data["Sbz1"]

        self.__data["Control"] = struct.unpack('<H', rawData.read(2))[0]
        self.Control = self.__data["Control"]

        self.__data["OffsetOwner"] = struct.unpack('<I', rawData.read(4))[0]
        self.OffsetOwner = self.__data["OffsetOwner"]

        self.__data["OffsetGroup"] = struct.unpack('<I', rawData.read(4))[0]
        self.OffsetGroup = self.__data["OffsetGroup"]

        self.__data["OffsetSacl"] = struct.unpack('<I', rawData.read(4))[0]
        self.OffsetSacl = self.__data["OffsetSacl"]

        self.__data["OffsetDacl"] = struct.unpack('<I', rawData.read(4))[0]
        self.OffsetDacl = self.__data["OffsetDacl"]

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        indent_prompt = "  │ " * indent
        print("%s<NTSecurityDescriptor_Header at offset \x1b[95m0x%x\x1b[0m (size=\x1b[95m0x%x\x1b[0m)>" % (indent_prompt, offset, self.bytesize))
        print("%s  │ \x1b[93mRevision\x1b[0m    : \x1b[96m0x%02x\x1b[0m" % (indent_prompt, self.__data["Revision"]))
        print("%s  │ \x1b[93mSbz1\x1b[0m        : \x1b[96m0x%02x\x1b[0m" % (indent_prompt, self.__data["Sbz1"]))
        print("%s  │ \x1b[93mControl\x1b[0m     : \x1b[96m0x%04x\x1b[0m" % (indent_prompt, self.__data["Control"]))
        print("%s  │ \x1b[93mOffsetOwner\x1b[0m : \x1b[96m0x%08x\x1b[0m" % (indent_prompt, self.__data["OffsetOwner"]))
        print("%s  │ \x1b[93mOffsetGroup\x1b[0m : \x1b[96m0x%08x\x1b[0m" % (indent_prompt, self.__data["OffsetGroup"]))
        print("%s  │ \x1b[93mOffsetSacl\x1b[0m  : \x1b[96m0x%08x\x1b[0m" % (indent_prompt, self.__data["OffsetSacl"]))
        print("%s  │ \x1b[93mOffsetDacl\x1b[0m  : \x1b[96m0x%08x\x1b[0m" % (indent_prompt, self.__data["OffsetDacl"]))
        print(''.join(["  │ "]*indent + ["  └─"]))

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def keys(self):
        return self.__data.keys()


class NTSecurityDescriptor(object):
    def __init__(self, value, verbose=False):
        self.value = value
        # Properties of this section
        self.header = None
        self.dacl = None
        self.sacl = None
        self.owner = None
        self.group = None
        self.verbose = verbose
        # 
        self.parse()

    def parse(self):
        if self.verbose:
            print("[>] Parsing %s\n  | value: %s" % (__class__, binascii.hexlify(self.value)))
        self.header = NTSecurityDescriptor_Header(value=self.value, verbose=self.verbose)
        self.value = self.value[self.header.bytesize:]

        # Parse OwnerSID if present
        if self.header.OffsetOwner == 0:
            self.owner = None
        else:
            self.owner = OwnerSID(
                value=self.value[self.header.OffsetOwner-self.header.bytesize:], 
                verbose=self.verbose
            )

        # Parse GroupSID if present
        if self.header.OffsetGroup == 0:
            self.group = None
        else:
            self.group = GroupSID(
                value=self.value[self.header.OffsetGroup-self.header.bytesize:], 
                verbose=self.verbose
            )

        # Parse DACL if present
        if self.header.OffsetDacl == 0:
            self.dacl = None
        else:
            self.dacl = DiscretionaryAccessControlList(
                value=self.value[self.header.OffsetDacl-self.header.bytesize:], 
                verbose=self.verbose
            )
        
        # Parse SACL if present
        if self.header.OffsetSacl == 0:
            self.sacl = None
        else:
            self.sacl = SystemAccessControlList(
                value=self.value[self.header.OffsetSacl-self.header.bytesize:], 
                verbose=self.verbose
            )

        if self.verbose:
            self.describe()

    def describe(self, offset=0, indent=0):
        print("<NTSecurityDescriptor>")
        self.header.describe(offset=offset, indent=indent+1)
        offset += self.header.bytesize
        if self.header.OffsetDacl < self.header.OffsetSacl:
            # Print DACL
            if self.dacl is not None:
                self.dacl.describe(offset=self.header.OffsetDacl, indent=indent+1)
            else:
                print("%s<DiscretionaryAccessControlList is \x1b[91mnot present\x1b[0m>" % ("  │ " * (indent+1)))
                print("%s  └─" % ("  │ " * (indent+1)))
            # Print SACL
            if self.sacl is not None:
                self.sacl.describe(offset=self.header.OffsetSacl, indent=indent+1)
            else:
                print("%s<SystemAccessControlList is \x1b[91mnot present\x1b[0m>" % ("  │ " * (indent+1)))
                print("%s  └─" % ("  │ " * (indent+1)))
        else:
            # Print SACL
            if self.sacl is not None:
                self.sacl.describe(offset=self.header.OffsetSacl, indent=indent+1)
            else:
                print("%s<SystemAccessControlList is \x1b[91mnot present\x1b[0m>" % ("  │ " * (indent+1)))
                print("%s  └─" % ("  │ " * (indent+1)))
            # Print DACL
            if self.dacl is not None:
                self.dacl.describe(offset=self.header.OffsetDacl, indent=indent+1)
            else:
                print("%s<DiscretionaryAccessControlList is \x1b[91mnot present\x1b[0m>" % ("  │ " * (indent+1)))
                print("%s  └─" % ("  │ " * (indent+1)))
        print("  └─")


def parseArgs():
    parser = argparse.ArgumentParser(add_help=True, description="Parse and describe the contents of a raw ntSecurityDescriptor structure")

    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Verbose mode. (default: False)")

    parser.add_argument("value", type=str, help="The value to be described by the NTSecurityDescriptor")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


if __name__ == "__main__":
    options = parseArgs()

    if os.path.isfile(options.value):
        print("[+] Loading ntSecurityDescriptor from file '%s'" % options.value)
        filename = options.value
        options.value = open(filename, 'r').read().strip()
    
    if re.compile(r'^[0-9a-fA-F]+$').match(options.value):
        options.value = binascii.unhexlify(options.value)

    ntsd = NTSecurityDescriptor(
        value=options.value, 
        verbose=options.verbose
    )

    if options.verbose:
        print("[>] Final result " + "".center(80,"="))

    ntsd.describe()