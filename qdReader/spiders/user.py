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
                'name': 'oneto160',
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
            },
            {
                'name': 'yyn861005',
                'password': '1212aaq'
            },
            {
                'name': 'qq376050902',
                'password': '1212aaq'
            },
            {
                'name': 'liu219475',
                'password': '1212aaq'
            },
            {
                'name': 'leleaishe',
                'password': '1212aaq'
            },
            {
                'name': 'haw511022',
                'password': '1212aaq'
            },
            {
                'name': 'q498937510',
                'password': '1212aaq'
            },
            {
                'name': 'wwhb70',
                'password': '1212aaq'
            },
            {
                'name': 'damujixiao',
                'password': '1212aaq'
            },
            {
                'name': 'ft40792',
                'password': '1212aaq'
            },
            {
                'name': 'kaimerry',
                'password': '1212aaq'
            },
            {
                'name': 'chenenke',
                'password': '1212aaq'
            },
            {
                'name': 'guochi918',
                'password': '1212aaq'
            },
            {
                'name': 'zcy7058619',
                'password': '1212aaq'
            },
            {
                'name': 'lcs3088',
                'password': '1212aaq'
            },
            {
                'name': 'zhangjieairh',
                'password': '1212aaq'
            },
            {
                'name': 'yan12000',
                'password': '1212aaq'
            },
            {
                'name': 'whitehcg',
                'password': '1212aaq'
            },
            {
                'name': 'aectxuen',
                'password': '1212aaq'
            },
            {
                'name': 'czh216507',
                'password': '1212aaq'
            },
            {
                'name': 'ljdrw123456',
                'password': '1212aaq'
            },
            {
                'name': 'ennoable',
                'password': '1212aaq'
            },
            {
                'name': 'longshen1915',
                'password': '1212aaq'
            }
        ]
        import random
        i = random.randint(0, len(account_list) - 1)
        return account_list[i]
