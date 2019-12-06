class User:
    def __init__(self):
        account = self.getAccount()
        self.name = account['name']
        self.password = account['password']

    # def __init__(self, name, password):
    #     self.name = name
    #     self.password = password

    def getAccount(self):
        account_list = [
            {
                'name': 'xuelong1012',
                'password': '1212aaq'
            },
            {
                'name': 'wf9822',
                'password': '1212aaq'
            },
            {
                'name': 'jack817817',
                'password': '1212aaq'
            },
            {
                'name': 'onto160',
                'password': '1212aaq'
            },
            {
                'name': 'yswhviqm',
                'password': '1212aaq'
            },
            {
                'name': 'azechj',
                'password': '1212aaq'
            },
            {
                'name': 's2030200692',
                'password': '1212aaq'
            },
            {
                'name': 'zjlxmp',
                'password': '1212aaq'
            },
            {
                'name': 'junzhanghz',
                'password': '1212aaq'
            },
            {
                'name': 'pk781126',
                'password': '1212aaq'
            },
            {
                'name': 'a461long',
                'password': '1212aaq'
            },
            {
                'name': 'zj1382',
                'password': '1212aaq'
            }
        ]
        import random
        i = random.randint(0, len(account_list) - 1)
        return account_list[i]
