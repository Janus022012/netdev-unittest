

class Device:
    def __init__(self, host_name, ip_address, manufacturer_name, device_name, version, port_name,
                 baudrate, login_id, login_password, admin_password):
        self._host_name = host_name
        self._ip_address = ip_address
        self._manufacturer_name = manufacturer_name
        self._device_name = device_name
        self._version = version
        self._port_name = port_name
        self._baudrate = baudrate
        self._login_id = login_id
        self._login_password = login_password
        self._admin_password = admin_password

    def __str__(self):
        return self.host_name

    @property
    def host_name(self):
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        self._host_name = host_name

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        self._ip_address = ip_address

    @property
    def manufacturer_name(self):
        return self._manufacturer_name

    @manufacturer_name.setter
    def manufacturer_name(self, manufacturer_name):
        self._manufacturer_name = manufacturer_name

    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, device_name):
        self._device_name = device_name

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def port_name(self):
        return self._port_name

    @port_name.setter
    def port_name(self, port_name):
        self._port_name = port_name

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        self._baudrate = baudrate

    @property
    def login_id(self):
        return self._login_id

    @login_id.setter
    def login_id(self, login_id):
        self._login_id = login_id

    @property
    def login_password(self):
        return self._login_password

    @login_password.setter
    def login_password(self, login_password):
        self._login_password = login_password

    @property
    def admin_password(self):
        return self._admin_password

    @admin_password.setter
    def admin_password(self, admin_password):
        self._admin_password = admin_password
