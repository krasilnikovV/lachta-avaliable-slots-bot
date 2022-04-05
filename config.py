from os import environ

is_online = bool(environ.get("IS_ONLINE", 0))
oms = bool(environ.get("OMS", 0))
