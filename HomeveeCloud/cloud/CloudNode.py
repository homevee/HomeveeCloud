import json

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.protocol.models import CloudToDeviceMethod

from HomeveeCloud.cloud.Helper.Utils import Utils

METHOD_PROCESS_DATA = "ProcessData"

class CloudNode():

    def __init__(self, host_name, shared_access_key_name, shared_access_key):
        self.host_name = host_name
        self.shared_access_key_name = shared_access_key_name
        self.shared_access_key = shared_access_key

        self.connection_string = "HostName="+self.host_name+";SharedAccessKeyName="+\
                                 self.shared_access_key_name+";SharedAccessKey="+self.shared_access_key

        # Create IoTHubRegistryManager
        self.registry_manager = IoTHubRegistryManager(self.connection_string)

        return

    def send_to_homevee_hub(self, remote_id, data):
        print(remote_id, data)

        if(not isinstance(data, str)):
            args = json.dumps(data)
        else:
            args = data

        deviceMethod = CloudToDeviceMethod(method_name=METHOD_PROCESS_DATA, payload=args)
        response = self.registry_manager.invoke_device_method(remote_id, deviceMethod)
        return response.payload

    @staticmethod
    def init_cloud_node():
        data = Utils.get_config_data()

        host_name = data['azure_host']
        shared_access_key_name = data['azure_access_key_name']
        shared_access_key = data['azure_access_key']

        cloud_node = CloudNode(host_name, shared_access_key_name, shared_access_key)
        return cloud_node

if __name__ == "__main__":
    cloud_node = CloudNode.init_cloud_node()

    data = {"action": "login", "username": "sascha", "password": "4a456a59"}
    response = cloud_node.send_to_homevee_hub("VX6FLAYZN", data)

    print(response)