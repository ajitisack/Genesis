
from configparser import ConfigParser
from configparser import ExtendedInterpolation

class Config():

    def __init__(self):
        cp = ConfigParser(interpolation=ExtendedInterpolation())
        cp.read("./stockdata/config.ini")
        # cp.read("config.ini")
        for section in cp.sections():
            for k,v in cp.items(section):
                # print(f"self.{k} = '{v}'")
                exec(f"self.{k} = r'{v}'")
