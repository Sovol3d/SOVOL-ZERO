# Copyright (C) 2022 igo95862, bernhardkaindl

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
from typing import Any, Dict, Tuple

# Type aliases for network connection settings and properties

# "Any" might be str, int, bool (e.g. autoconnect), List[Ip] and maybe others
NetworkManagerSetting = Tuple[str, Any]

# A settings domain, e.g. ipv4.*, ipv6.*, 802-11-wireless-security.*, etc:
NetworkManagerSettingsDomain = Dict[str, NetworkManagerSetting]

# All settings and properties of a connection, e.g. returned by get_settings()
NetworkManagerConnectionProperties = Dict[str, NetworkManagerSettingsDomain]

# All settings and properties of a connection, but without dbus signatures
SettingsDict = Dict[str, Dict[str, Any]]
