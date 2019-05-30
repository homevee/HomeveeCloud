import json

from iothub_client.iothub_client import IoTHubTransportProvider
from iothub_service_client.iothub_service_client import IoTHubDeviceMethod

from cloud.Helper.Utils import Utils

METHOD_PROCESS_DATA = "ProcessData"

class CloudNode():

    def __init__(self, host_name, shared_access_key_name, shared_access_key):
        self.protocol = IoTHubTransportProvider.MQTT
        self.host_name = host_name
        self.shared_access_key_name = shared_access_key_name
        self.shared_access_key = shared_access_key

        self.connection_string = "HostName="+self.host_name+";SharedAccessKeyName="+\
                                 self.shared_access_key_name+";SharedAccessKey="+self.shared_access_key

        self.timeout = 5000

        self.iothub_device_method = IoTHubDeviceMethod(self.connection_string)

        return

    def send_to_homevee_hub(self, remote_id, data):
        print(remote_id, data)

        if(not isinstance(data, str)):
            args = json.dumps(data)
        else:
            args = data

        response = self.iothub_device_method.invoke(remote_id, METHOD_PROCESS_DATA, args, self.timeout)
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