
from configparser import ConfigParser
from configparser import ExtendedInterpolation

cp = ConfigParser(interpolation=ExtendedInterpolation())
cp.read("stockdata/config.ini")
cp.get('database', 'dbfile')
cp['database']['dbfile']
