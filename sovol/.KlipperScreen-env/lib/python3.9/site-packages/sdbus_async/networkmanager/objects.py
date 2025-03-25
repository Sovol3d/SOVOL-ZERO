

# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2020, 2021 igo95862

# This file is part of python-sdbus

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from __future__ import annotations

from typing import List, Optional

from sdbus.sd_bus_internals import SdBus

from .interfaces_devices import (
    NetworkManagerDeviceBluetoothInterfaceAsync,
    NetworkManagerDeviceBondInterfaceAsync,
    NetworkManagerDeviceBridgeInterfaceAsync,
    NetworkManagerDeviceGenericInterfaceAsync,
    NetworkManagerDeviceInterfaceAsync,
    NetworkManagerDeviceIPTunnelInterfaceAsync,
    NetworkManagerDeviceMacsecInterfaceAsync,
    NetworkManagerDeviceMacvlanInterfaceAsync,
    NetworkManagerDeviceModemInterfaceAsync,
    NetworkManagerDeviceOlpcMeshInterfaceAsync,
    NetworkManagerDeviceOvsBridgeInterfaceAsync,
    NetworkManagerDeviceOvsPortInterfaceAsync,
    NetworkManagerDeviceStatisticsInterfaceAsync,
    NetworkManagerDeviceTeamInterfaceAsync,
    NetworkManagerDeviceTunInterfaceAsync,
    NetworkManagerDeviceVethInterfaceAsync,
    NetworkManagerDeviceVlanInterfaceAsync,
    NetworkManagerDeviceVrfInterfaceAsync,
    NetworkManagerDeviceVxlanInterfaceAsync,
    NetworkManagerDeviceWifiP2PInterfaceAsync,
    NetworkManagerDeviceWiredInterfaceAsync,
    NetworkManagerDeviceWireGuardInterfaceAsync,
    NetworkManagerDeviceWirelessInterfaceAsync,
    NetworkManagerLoopbackInterfaceAsync,
    NetworkManagerPPPInterfaceAsync,
)
from .interfaces_other import (
    NetworkManagerAccessPointInterfaceAsync,
    NetworkManagerCheckpointInterfaceAsync,
    NetworkManagerConnectionActiveInterfaceAsync,
    NetworkManagerDHCP4ConfigInterfaceAsync,
    NetworkManagerDHCP6ConfigInterfaceAsync,
    NetworkManagerDnsManagerInterfaceAsync,
    NetworkManagerInterfaceAsync,
    NetworkManagerIP4ConfigInterfaceAsync,
    NetworkManagerIP6ConfigInterfaceAsync,
    NetworkManagerSecretAgentManagerInterfaceAsync,
    NetworkManagerSettingsConnectionInterfaceAsync,
    NetworkManagerSettingsInterfaceAsync,
    NetworkManagerVPNConnectionInterfaceAsync,
    NetworkManagerWifiP2PPeerInterfaceAsync,
)
from .types import NetworkManagerConnectionProperties

NETWORK_MANAGER_SERVICE_NAME = 'org.freedesktop.NetworkManager'


class NetworkManager(NetworkManagerInterfaceAsync):
    """Network Manager main object

    Implements :py:class:`NetworkManagerInterfaceAsync`

    Service name ``'org.freedesktop.NetworkManager'``
    and object path ``/org/freedesktop/NetworkManager`` is predetermined.
    """

    def __init__(self, bus: Optional[SdBus] = None) -> None:
        """
        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            '/org/freedesktop/NetworkManager',
            bus)


class NetworkManagerAgentManager(
        NetworkManagerSecretAgentManagerInterfaceAsync):
    """NetworkManager secrets manager

    Implements :py:class:`NetworkManagerSecretAgentManagerInterfaceAsync`.

    Service name ``'org.freedesktop.NetworkManager'``
    and object path ``/org/freedesktop/NetworkManager/AgentManager``
    is predetermined.
    """

    def __init__(self, bus: Optional[SdBus] = None) -> None:
        """
        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            '/org/freedesktop/NetworkManager/AgentManager',
            bus)


class NetworkManagerDnsManager(NetworkManagerDnsManagerInterfaceAsync):
    """NetworkManager DNS manager

    Implements :py:class:`NetworkManagerDnsManagerInterfaceAsync`.

    Service name ``'org.freedesktop.NetworkManager'``
    and object path ``/org/freedesktop/NetworkManager/DnsManager``
    is predetermined.
    """

    def __init__(self, bus: Optional[SdBus] = None) -> None:
        """
        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            '/org/freedesktop/NetworkManager/DnsManager',
            bus)


class NetworkManagerSettings(NetworkManagerSettingsInterfaceAsync):
    """NetworkManager settings

    Implements :py:class:`NetworkManagerSettingsInterfaceAsync`.

    Service name ``'org.freedesktop.NetworkManager'``
    and object path ``/org/freedesktop/NetworkManager/DnsManager``
    is predetermined.
    """

    def __init__(self, bus: Optional[SdBus] = None) -> None:
        """
        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            '/org/freedesktop/NetworkManager/Settings',
            bus)

    async def get_connections_by_id(self, connection_id: str) -> List[str]:
        """Helper method to get a list of connection profile paths
        which use the given connection identifier.

        :param str connection_id: The connection identifier of the connections,
                                  e.g. "Wired connection 1"
        :return: List of connection profile paths using the given identifier.
        """
        connection_paths_with_matching_id = []
        connection_paths: List[str] = await self.connections
        for connection_path in connection_paths:
            settings = NetworkConnectionSettings(connection_path)
            settings_properites = await settings.get_settings()
            # settings_properites["connection"]["id"][1] gives the id value:
            if settings_properites["connection"]["id"][1] == connection_id:
                connection_paths_with_matching_id.append(connection_path)
        return connection_paths_with_matching_id

    async def get_settings_by_uuid(
        self, connection_uuid: str
    ) -> NetworkManagerConnectionProperties:
        """Helper to get a nested settings dict of a connection profile by uuid.

        :param str connection_uuid: The connection uuid of the connection profile
        :return: Nested dictionary of all settings of the given connection profile
        """
        connection = await self.get_connection_by_uuid(connection_uuid)
        connection_manager = NetworkConnectionSettings(connection)
        connection_settings = await connection_manager.get_settings()
        return connection_settings

    async def delete_connection_by_uuid(self, connection_uuid: str) -> None:
        """Helper to delete a connection profile identified by the connection uuid.

        :param str connection_uuid: The connection uuid of the connection profile
        """
        conn_dbus_path = await self.get_connection_by_uuid(connection_uuid)
        connection_settings_manager = NetworkConnectionSettings(conn_dbus_path)
        await connection_settings_manager.delete()


class NetworkConnectionSettings(
        NetworkManagerSettingsConnectionInterfaceAsync):
    """Setting of specific connection

    Implements :py:class:`NetworkManagerSettingsConnectionInterfaceAsync`
    """

    def __init__(self, settings_path: str,
                 bus: Optional[SdBus] = None) -> None:
        """
        :param settings_path: D-Bus path to settings object. \
            Usually obtained from \
            :py:attr:`NetworkManagerDeviceInterfaceAsync.active_connection`

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            settings_path,
            bus)


class NetworkDeviceGeneric(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceGenericInterfaceAsync):
    """Generic device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceGenericInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceWired(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceWiredInterfaceAsync):
    """Ethernet device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceWiredInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceWireless(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceWirelessInterfaceAsync):
    """WiFi device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceWirelessInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceBluetooth(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceBluetoothInterfaceAsync):
    """Bluetooth device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceBluetoothInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceBond(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceBondInterfaceAsync):
    """Bond device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceBondInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceBridge(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceBridgeInterfaceAsync):
    """Bridge device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceBridgeInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceIpTunnel(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceIPTunnelInterfaceAsync):
    """Generic device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceIPTunnelInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceMacsec(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceMacsecInterfaceAsync):
    """Macsec device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceMacsecInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceMacvlan(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceMacvlanInterfaceAsync):
    """Macvlan device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceMacvlanInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceModem(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceModemInterfaceAsync):
    """Generic device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceModemInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceOlpcMesh(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceOlpcMeshInterfaceAsync):
    """OLPC wireless mesh device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceOlpcMeshInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceOpenVSwitchBridge(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceOvsBridgeInterfaceAsync):
    """Open vSwitch bridge device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceOvsBridgeInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceOpenVSwitchPort(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceOvsPortInterfaceAsync):
    """Open vSwitch port device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceOvsPortInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceTeam(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceTeamInterfaceAsync):
    """Team device (special Bond device for NetworkManager)

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceTeamInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceTun(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceTunInterfaceAsync):
    """TUN device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceTunInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceVeth(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceVethInterfaceAsync):
    """Virtual Ethernet device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceVethInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceVlan(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceVlanInterfaceAsync):
    """VLAN device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceVlanInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceVrf(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceVrfInterfaceAsync):
    """VRF (virtual routing) device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceVrfInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceVxlan(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceVxlanInterfaceAsync):
    """VXLAN device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceVxlanInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceWifiP2P(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceWifiP2PInterfaceAsync):
    """Wifi Peer-to-Peer (P2P) device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceWifiP2PInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceWireGuard(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerDeviceWireGuardInterfaceAsync):
    """Generic device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerDeviceWireGuardInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDevicePPP(
        NetworkManagerDeviceInterfaceAsync,
        NetworkManagerDeviceStatisticsInterfaceAsync,
        NetworkManagerPPPInterfaceAsync):
    """PPP device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerPPPInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class NetworkDeviceLoopback(
    NetworkManagerDeviceInterfaceAsync,
    NetworkManagerDeviceStatisticsInterfaceAsync,
    NetworkManagerLoopbackInterfaceAsync,
):
    """Loopback device

    Implements :py:class:`NetworkManagerDeviceInterfaceAsync`, \
    :py:class:`NetworkManagerDeviceStatisticsInterfaceAsync` and \
    :py:class:`NetworkManagerLoopbackInterfaceAsync`
    """

    def __init__(self, device_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param device_path: D-Bus path to device object. \
            Obtained from \
            :py:meth:`NetworkManagerInterface.get_devices` or \
            :py:meth:`NetworkManagerInterface.get_device_by_ip_iface`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            device_path,
            bus)


class ActiveConnection(NetworkManagerConnectionActiveInterfaceAsync):
    """Active connection object

    Implements :py:class:`NetworkManagerConnectionActiveInterfaceAsync`
    """

    def __init__(self, connection_path: str,
                 bus: Optional[SdBus] = None) -> None:
        """

        :param connection_path: D-Bus path to connection object. \
            Obtained from \
            :py:meth:`NetworkManagerDeviceInterfaceAsync.active_connection`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            connection_path,
            bus)


class ActiveVPNConnection(
        ActiveConnection,
        NetworkManagerVPNConnectionInterfaceAsync):
    """Active VPN connection object

    Implements :py:class:`NetworkManagerConnectionActiveInterfaceAsync`
    and :py:class:`NetworkManagerVPNConnectionInterfaceAsync`
    """
    ...


class IPv4Config(NetworkManagerIP4ConfigInterfaceAsync):
    """IPv4 configuration interface

    Implements :py:class:`NetworkManagerIP4ConfigInterfaceAsync`
    """

    def __init__(self, ip4_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param ip4_path: D-Bus path to IPv4 config object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceInterfaceAsync.ip4_config`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            ip4_path,
            bus)


class IPv6Config(NetworkManagerIP6ConfigInterfaceAsync):
    """IPv6 configuration interface

    Implements :py:class:`NetworkManagerIP6ConfigInterfaceAsync`
    """

    def __init__(self, ip6_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param ip6_path: D-Bus path to IPv6 config object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceInterfaceAsync.ip4_config`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            ip6_path,
            bus)


class DHCPv4Config(NetworkManagerDHCP4ConfigInterfaceAsync):
    """DHCPv4 configuration interface

    Implements :py:class:`NetworkManagerDHCP4ConfigInterfaceAsync`
    """

    def __init__(self, dhcp4_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param dhcp4_path: D-Bus path to DHCPv4 config object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceInterfaceAsync.dhcp4_config`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            dhcp4_path,
            bus)


class DHCPv6Config(NetworkManagerDHCP6ConfigInterfaceAsync):
    """DHCPv6 configuration interface

    Implements :py:class:`NetworkManagerDHCP6ConfigInterfaceAsync`
    """

    def __init__(self, dhcpv6_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param dhcpv6_path: D-Bus path to DHCPv6 config object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceInterfaceAsync.dhcp6_config`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            dhcpv6_path,
            bus)


class AccessPoint(NetworkManagerAccessPointInterfaceAsync):
    """Access Point (WiFi point) object

    Implements :py:class:`NetworkManagerAccessPointInterfaceAsync`
    """

    def __init__(self, point_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param point_path: D-Bus path to access point object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceWirelessInterfaceAsync.access_points`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            point_path,
            bus)


class WiFiP2PPeer(NetworkManagerWifiP2PPeerInterfaceAsync):
    """WiFi peer object

    Implements :py:class:`NetworkManagerWifiP2PPeerInterfaceAsync`
    """

    def __init__(self, peer_path: str, bus: Optional[SdBus] = None) -> None:
        """

        :param peer_path: D-Bus path to access point object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceWifiP2PInterfaceAsync.peers`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            peer_path,
            bus)


class ConfigCheckpoint(NetworkManagerCheckpointInterfaceAsync):
    """Configuration checkpoint interface

    Implements :py:class:`NetworkManagerCheckpointInterfaceAsync`
    """

    def __init__(self, checkpoint_path: str,
                 bus: Optional[SdBus] = None) -> None:
        """

        :param checkpoint_path: D-Bus path to access point object. \
            Obtained from \
            :py:attr:`NetworkManagerDeviceWifiP2PInterfaceAsync.checkpoint_create`.

        :param bus: You probably want to set default bus to system bus \
            or pass system bus directly.
        """
        super().__init__()
        self._connect(
            NETWORK_MANAGER_SERVICE_NAME,
            checkpoint_path,
            bus)
