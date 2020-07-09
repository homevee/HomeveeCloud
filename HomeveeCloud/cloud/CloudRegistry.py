from azure.iot.hub import IoTHubRegistryManager

from HomeveeCloud.cloud.Helper.Utils import Utils


class CloudRegistry:
    def __init__(self, host_name, shared_access_key_name, shared_access_key):
        self.host_name = host_name
        self.shared_access_key_name = shared_access_key_name
        self.shared_access_key = shared_access_key
        self.connection_string = "HostName="+self.host_name+";SharedAccessKeyName="+\
                                 self.shared_access_key_name+";SharedAccessKey="+self.shared_access_key
        self.iothub_registry_manager = IoTHubRegistryManager(str(self.connection_string))
        return

    def generate_keys(self) -> tuple:
        """
        Generates a primary and secondary key
        :return: a tuple with primary and secondary key
        """
        primary_key = "primary"
        secondary_key = "secondary"
        return primary_key, secondary_key

    def generate_remote_id(self) -> str:
        """
        Generates a new remote id
        :return: the remote id
        """
        remote_id = "remote_id"
        return remote_id

    def register_device(self, remote_id: str):
        """
        Registers a new device
        :param remote_id: the remote id
        :return:
        """
        try:
            remote_id = self.generate_remote_id()
            status = "enabled"
            primary_key, secondary_key = self.generate_keys()
            new_device = self.iothub_registry_manager.create_device_with_sas(remote_id, primary_key, secondary_key, status)
            return new_device
        except Exception as iothub_error:
            print("Unexpected error {0}".format(iothub_error))
            return
        except KeyboardInterrupt:
            print("IoTHubRegistryManager sample stopped")

    def update_device(self, remote_id) -> str:
        """
        Update the hub with the given remote id
        :param remote_id: the remote id
        :return:
        """
        try:
            primary_key, secondary_key = self.generate_keys()
            status = "enabled"
            self.iothub_registry_manager.update_device_with_sas(remote_id, remote_id, primary_key, secondary_key, status)
            updated_device = self.iothub_registry_manager.get_device(remote_id)
            return updated_device
        except Exception as iothub_error:
            print("Unexpected error {0}".format(iothub_error))
            return
        except KeyboardInterrupt:
            print("IoTHubRegistryManager sample stopped")


if __name__ == "__main__":
    data = Utils.get_config_data()

    host_name = data['azure_host']
    shared_access_key_name = data['azure_access_key_name']
    shared_access_key = data['azure_access_key']

    registry = CloudRegistry(host_name, shared_access_key_name, shared_access_key)
    registry.register_device("test_device_1")