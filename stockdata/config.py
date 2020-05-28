import os
from configparser import ConfigParser
from configparser import ExtendedInterpolation

class Config():

    def __init__(self):
        cp = ConfigParser(interpolation=ExtendedInterpolation())
        # cp.read(r'C:/ajit/stockanalysis/stockdata/config.ini')
        config_file = f'{os.path.dirname(__file__)}/config.ini'
        cp.read(config_file)
        for section in cp.sections():
            for k,v in cp.items(section):
                # print(f"self.{k} = '{v}'")
                exec(f"self.{k} = r'{v}'")
