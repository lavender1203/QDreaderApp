class Device:
    def __init__(self):
        device = self.getDevice()
        self.device_name = device['device_name']

    def getDevice(self):
        devices = [
            {
                'devicename': 'Honor 8',
                'devicetype': 'Huawei_FRD-AL00',
                'qimei': '43757bd7111bb806',
                'imei': '862679037204730',
            },
            {
                'devicename': 'Nexus 5',
                'devicetype': 'google_Nexus 5',
                'qimei': '194adf233363c032',
                'imei': '359250052265715',
            },
        ]

        import random
        i = random.randint(0, len(devices))
        return devices[i]
