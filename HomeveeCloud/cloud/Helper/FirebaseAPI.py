from pyfcm import FCMNotification

from HomeveeCloud.cloud.Helper.ServerData import ServerData


class FirebaseAPI:
    def __init__(self):
        return

    @staticmethod
    def send_notification(registration_ids, message_body):
        api_key = ServerData.get("FIREBASE_TOKEN")

        push_service = FCMNotification(api_key=api_key)
        result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                            data_message=message_body)
        return result