# SPDX-License-Identifier: LGPL-2.1-or-later
from __future__ import annotations

from dataclasses import dataclass, fields
from functools import lru_cache
from typing import Any, ClassVar, Dict, List, Type, cast

from ..types import NetworkManagerSettingsDomain


@dataclass
class NetworkManagerSettingsMixin:
    secret_fields_names: ClassVar[List[str]] = []
    secret_name: ClassVar[str] = ''

    def to_dbus(self) -> NetworkManagerSettingsDomain:
        """Return a dbus dictionary for NetworkManager to add/update profiles

        The key names provided are exactly as documented in these tables:
        https://networkmanager.dev/docs/api/latest/nm-settings-dbus.html
        """
        new_dict: NetworkManagerSettingsDomain = {}

        for x in fields(self):
            value = getattr(self, x.name)
            if value is None:
                continue

            if x.metadata['dbus_type'] == 'aa{sv}':
                packed_variant = ('aa{sv}', [x.to_dbus() for x in value])
            else:
                packed_variant = (x.metadata['dbus_type'], value)

            new_dict[x.metadata['dbus_name']] = packed_variant

        return new_dict

    def to_settings_dict(self, defaults: bool = False) -> Dict[str, Any]:
        """Return a simple dictionary using the same key names like the dbus
        dict from to_dbus(), but without the dbus signatures returned by it.

        The key names provided are exactly as documented in these tables:
        https://networkmanager.dev/docs/api/latest/nm-settings-dbus.html

        Contrary to dataclasses.asdict(), it provides the original dbus keys,
        e.g. with numerical prefixes like "802-11-", dashes, and "id"/"type".

        In addition, it can be selected if defaults shall be omitted in output,
        like NetworkConnectionSettings.get_settings() omits default values:

        Because of this, all NetworkManager clients which read profiles have
        to have hard-coded knowledge of these defaults. By this omission, they
        are part of the stable API: They can be relied upon to never change.
        Omitting the defaults makes the typical output really small for review.
        """
        new_dict = {}
        for x in fields(self):
            value = getattr(self, x.name)
            if value in [None, {}, []]:
                continue
            if not defaults and value == x.default:
                continue
            dbus_type = x.metadata['dbus_type']
            if dbus_type == 'aa{sv}':
                value = [x.to_settings_dict(defaults) for x in value]
            elif dbus_type == 'ay' and x.name == "ssid":
                value = value.decode('utf8')  # Make SSID JSON-serializable
            new_dict[x.metadata['dbus_name']] = value
        return new_dict

    @classmethod
    def _unpack_variant(cls, key: str, signature: str, value: Any) -> Any:
        if signature == 'aa{sv}':
            inner_class = cls.setting_name_to_inner_class(key)
            return [inner_class.from_dbus(x) for x in value]

        return value

    @classmethod
    def from_dbus(
        cls,
        dbus_dict: NetworkManagerSettingsDomain,
    ) -> NetworkManagerSettingsMixin:
        """TODO: Add proper docstring"""
        reverse_mapping = cls.setting_name_reverse_mapping()
        unvarianted_options = {}
        for k, v in dbus_dict.items():
            try:
                reverse_name = reverse_mapping[k]
            except KeyError:
                continue

            unvarianted_options[reverse_name] = cls._unpack_variant(k, *v)

        return cls(**unvarianted_options)

    @classmethod
    def from_dict(cls,
                  plain_dict: Dict[str, Any]
                  ) -> NetworkManagerSettingsMixin:
        options = {}
        for dataclass_field in fields(cls):
            dbus_name = dataclass_field.metadata["dbus_name"]
            if dbus_name in plain_dict:
                value = plain_dict[dbus_name]
                dbus_type = dataclass_field.metadata['dbus_type']
                if dbus_type == 'aa{sv}':
                    inner_class = cls.setting_name_to_inner_class(dbus_name)
                    value = [inner_class.from_dict(item) for item in value]
                elif dbus_type == 'ay' and isinstance(value, str):
                    # If byte array(e.g. ssid) was passed as string encode it:
                    value = value.encode('utf8')
                options[dataclass_field.name] = value
        return cls(**options)

    @classmethod
    @lru_cache(maxsize=None)
    def setting_name_reverse_mapping(cls) -> Dict[str, str]:
        return {f.metadata['dbus_name']: f.name for f in fields(cls)}

    @classmethod
    @lru_cache(maxsize=None)
    def setting_name_to_inner_class(cls, setting_name: str) -> Type[Any]:
        for x in fields(cls):
            if setting_name != x.metadata['dbus_name']:
                continue
            return cast(Type[Any], x.metadata['dbus_inner_class'])

        raise ValueError('Inner class not found')
