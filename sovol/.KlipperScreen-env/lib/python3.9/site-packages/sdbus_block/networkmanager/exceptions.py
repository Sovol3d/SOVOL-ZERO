# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2021 igo95862

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

from sdbus import DbusFailedError


class NetworkManagerBaseError(Exception):
    """Base of all NetworkManager errors."""


# Errors returned from the secret-agent manager.
class NmAgentManagerFailedError(DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = 'org.freedesktop.NetworkManager.AgentManager.Failed'


class NmAgentManagerPermissionDeniedError(
        DbusFailedError, NetworkManagerBaseError):
    """The caller does not have permission to register a secret agent,
    or is trying to register the same secret agent twice."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AgentManager.PermissionDenied'
    )


class NmAgentManagerInvalidIdentifierError(DbusFailedError):
    """The identifier is not a valid secret agent identifier."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AgentManager.InvalidIdentifier'
    )


class NmAgentManagerNotRegisteredError(
        DbusFailedError, NetworkManagerBaseError):
    """The caller tried to unregister an agent that was not registered."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AgentManager.NotRegistered'
    )


class NmAgentManagerNoSecretsError(
        DbusFailedError, NetworkManagerBaseError):
    """No secret agent returned secrets for this request."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AgentManager.NoSecrets'
    )


class NmAgentManagerUserCanceledError(
        DbusFailedError, NetworkManagerBaseError):
    """The user canceled the secrets request."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AgentManager.UserCanceled'
    )


# Errors returned by Connection objects.
class NmConnectionFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.Failed'
    )


class NmConnectionSettingNotFoundError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection object did not contain the specified Setting object."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.SettingNotFound'
    )


class NmConnectionPropertyNotFoundError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection object did not contain the requested Setting property"""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.PropertyNotFound'
    )


class NmConnectionPropertyNotSecretError(
        DbusFailedError, NetworkManagerBaseError):
    """An operation which requires a secret was attempted on a
    non-secret property."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.PropertyNotSecret'
    )


class NmConnectionMissingSettingError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection object is missing an Setting which is required
    for its configuration."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.MissingSetting'
    )


class NmConnectionInvalidSettingError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection object contains an invalid or inappropriate Setting."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.InvalidSetting'
    )


class NmConnectionMissingPropertyError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection object is invalid because it is missing a
    required property."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.MissingProperty'
    )


class NmConnectionInvalidPropertyError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection object is invalid because a property has an invalid value."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Connection.InvalidProperty'
    )


# Device-related errors.
class NmDeviceFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.Failed'
    )


class NmDeviceCreationFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """NetworkManager failed to create the device."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.CreationFailed'
    )


class NmDeviceInvalidConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """The specified connection is not valid."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.InvalidConnection'
    )


class NmDeviceIncompatibleConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """Specified connection is not compatible with this device."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.IncompatibleConnection'
    )


class NmDeviceNotActiveError(
        DbusFailedError, NetworkManagerBaseError):
    """Device does not have an active connection."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.NotActive'
    )


class NmDeviceNotSoftwareError(
        DbusFailedError, NetworkManagerBaseError):
    """Requested operation is only valid on software devices."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.NotSoftware'
    )


class NmDeviceNotAllowedError(
        DbusFailedError, NetworkManagerBaseError):
    """Requested operation is not allowed at this time."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.NotAllowed'
    )


class NmDeviceSpecificObjectNotFoundError(
        DbusFailedError, NetworkManagerBaseError):
    """Specific object in the activation request
    (eg, the AccessPoint or WimaxNsp) was not found."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.SpecificObjectNotFound'
    )


class NmDeviceVersionIdMismatchError(
        DbusFailedError, NetworkManagerBaseError):
    """Version id did not match."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.VersionIdMismatch'
    )


class NmDeviceMissingDependenciesError(
        DbusFailedError, NetworkManagerBaseError):
    """Requested operation could not be completed
    due to missing dependencies."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.MissingDependencies'
    )


class NmDeviceInvalidArgumentError(
        DbusFailedError, NetworkManagerBaseError):
    """Invalid argument.

    Since: 1.16."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Device.InvalidArgument'
    )


# Errors related to the main interface of NetworkManager.
class NetworkManagerFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Failed'
    )


class NetworkManagerPermissionDeniedError(
        DbusFailedError, NetworkManagerBaseError):
    """Permission denied."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.PermissionDenied'
    )


class NetworkManagerUnknownConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """The requested connection is not known."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.UnknownConnection'
    )


class NetworkManagerUnknownDeviceError(
        DbusFailedError, NetworkManagerBaseError):
    """The requested device is not known."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.UnknownDevice'
    )


class NetworkManagerConnectionNotAvailableError(
        DbusFailedError, NetworkManagerBaseError):
    """The requested connection cannot be activated at this time."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.ConnectionNotAvailable'
    )


class NetworkManagerConnectionNotActiveError(
        DbusFailedError, NetworkManagerBaseError):
    """The request could not be completed because a required connection
    is not active."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.ConnectionNotActive'
    )


class NetworkManagerConnectionAlreadyActiveError(
        DbusFailedError, NetworkManagerBaseError):
    """The connection to be activated was already active on another device."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.ConnectionAlreadyActive'
    )


class NetworkManagerDependencyFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """An activation request failed due to a dependency being unavailable."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.DependencyFailed'
    )


class NetworkManagerAlreadyAsleepOrAwakeError(
        DbusFailedError, NetworkManagerBaseError):
    """The manager is already in the requested sleep/wake state."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AlreadyAsleepOrAwake'
    )


class NetworkManagerAlreadyEnabledOrDisabledError(
        DbusFailedError, NetworkManagerBaseError):
    """The network is already enabled/disabled."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.AlreadyEnabledOrDisabled'
    )


class NetworkManagerUnknownLogLevelError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown log level in
    :py:func:`NetworkManagerInterfaceAsync.set_logging`."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.UnknownLogLevel'
    )


class NetworkManagerUnknownLogDomainError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown log domain in
    :py:func:`NetworkManagerInterfaceAsync.set_logging`."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.UnknownLogDomain'
    )


class NetworkManagerInvalidArgumentsError(
        DbusFailedError, NetworkManagerBaseError):
    """Invalid arguments for D-Bus request."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.InvalidArguments'
    )


class NetworkManagerMissingPluginError(
        DbusFailedError, NetworkManagerBaseError):
    """A plug-in was needed to complete the
    activation but is not available."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.MissingPlugin'
    )


# Errors that secret managers pass to NetworkManager
class NmSecretManagerFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.SecretManager.Failed'
    )


class NmSecretManagerPermissionDeniedError(
        DbusFailedError, NetworkManagerBaseError):
    """The caller (ie, NetworkManager) is
    not authorized to make this request."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.SecretManager.PermissionDenied'
    )


class NmSecretManagerInvalidConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection for which secrets were requested is invalid."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.SecretManager.InvalidConnection'
    )


class NmSecretManagerUserCanceledError(
        DbusFailedError, NetworkManagerBaseError):
    """Request was canceled by the user."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.SecretManager.UserCanceled'
    )


class NmSecretManagerAgentCanceledError(
        DbusFailedError, NetworkManagerBaseError):
    """Agent canceled the request because it was requested
    to do so by NetworkManager."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.SecretManager.AgentCanceled'
    )


class NmSecretManagerNoSecretsError(
        DbusFailedError, NetworkManagerBaseError):
    """The agent cannot find any secrets for this connection."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.SecretManager.NoSecrets'
    )


# Errors related to the settings/persistent
# configuration interface of NetworkManager.
class NmSettingsFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.Failed'
    )


class NmSettingsPermissionDeniedError(
        DbusFailedError, NetworkManagerBaseError):
    """Permission denied."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.PermissionDenied'
    )


class NmSettingsNotSupportedError(
        DbusFailedError, NetworkManagerBaseError):
    """Requested operation is not supported by any
    active settings backend."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.NotSupported'
    )


class NmSettingsInvalidConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection was invalid."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.InvalidConnection'
    )


class NmSettingsReadOnlyConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """Attempted to modify a read-only connection."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.ReadOnlyConnection'
    )


class NmSettingsUuidExistsError(
        DbusFailedError, NetworkManagerBaseError):
    """Connection with that UUID already exists."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.UuidExists'
    )


class NmSettingsInvalidHostnameError(
        DbusFailedError, NetworkManagerBaseError):
    """Attempted to set an invalid hostname."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.InvalidHostname'
    )


class NmSettingsInvalidArgumentsError(
        DbusFailedError, NetworkManagerBaseError):
    """Invalid arguments."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.Settings.InvalidArguments'
    )


# Returned by the VPN service plugin to indicate errors.
class NmVpnPluginFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Unknown or unspecified error."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.Failed'
    )


class NmVpnPluginStartingInProgressError(
        DbusFailedError, NetworkManagerBaseError):
    """Plugin is already starting and another connect
    request was received."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.StartingInProgress'
    )


class NmVpnPluginAlreadyStartedError(
        DbusFailedError, NetworkManagerBaseError):
    """Plugin is already connected and another connect
    request was received."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.AlreadyStarted'
    )


class NmVpnPluginStoppingInProgressError(
        DbusFailedError, NetworkManagerBaseError):
    """Plugin is already stopping and another stop
    request was received."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.StoppingInProgress'
    )


class NmVpnPluginAlreadyStoppedError(
        DbusFailedError, NetworkManagerBaseError):
    """Plugin is already stopped and another disconnect
    request was received."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.AlreadyStopped'
    )


class NmVpnPluginWrongStateError(
        DbusFailedError, NetworkManagerBaseError):
    """Operation could not be performed in this state."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.WrongState'
    )


class NmVpnPluginBadArgumentsError(
        DbusFailedError, NetworkManagerBaseError):
    """Operation could not be performed as the request contained
    malformed arguments, or arguments of unexpected type.

    Usually means that one of the VPN setting data items or secrets
    was not of the expected type (ie int, string, bool, etc).
    """
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.BadArguments'
    )


class NmVpnPluginLaunchFailedError(
        DbusFailedError, NetworkManagerBaseError):
    """Child process failed to launch."""
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.LaunchFailed'
    )


class NmVpnPluginInvalidConnectionError(
        DbusFailedError, NetworkManagerBaseError):
    """Operation could not be performed because the connection was invalid.

    Usually means that the connection's VPN setting was missing
    some required data item or secret.
    """
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.InvalidConnection'
    )


class NmVpnPluginInteractiveNotSupportedError(
        DbusFailedError, NetworkManagerBaseError):
    """Operation could not be performed as the plugin
    does not support interactive operations.

    Interactive operations such as
    :py:func:`NetworkManagerVPNPluginInterfaceAsync.connect_interactive`
    or :py:func:`NetworkManagerVPNPluginInterfaceAsync.new_secrets`.
    """
    dbus_error_name = (
        'org.freedesktop.NetworkManager.VPN.Error.InteractiveNotSupported'
    )
