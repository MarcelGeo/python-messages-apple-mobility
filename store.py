__STORE__ = {"exceptions": []}

def initStore(**kwargs):
  for key, value in kwargs.items():
    print(key)
    __STORE__[key] = value

def updateStore(**kwargs):
  for key, value in kwargs.items():
    if key in __STORE__:
      __STORE__[key] = value

def mapStore(key):
  if key in __STORE__:
    return __STORE__[key]
  else:
    return None