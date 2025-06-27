import sys
sys.path.insert(0, '../../../')

from ATV630Controller import ATV630Controller

class ATVModel(ATV630Controller):
    def __init__(self, ip_addr):
        super().__init__(ip_address = ip_addr)

if __name__ == '__main__':
    ATVModel("192.168.100.125")
