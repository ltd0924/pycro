from pycromanager import Bridge

with Bridge() as bridge:
    print(bridge.get_core())