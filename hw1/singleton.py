import ctypes

class SingletonWithNew:
    _entity = None

    def __new__(cls):
        if cls._entity is None:
            cls._entity = super().__new__(cls)
        return cls._entity

class SingletonWithCtypes:
    _entity_address = ctypes.c_void_p(0)

    def __new__(cls):
        if not cls._entity_address.value:
            instance = super().__new__(cls)
            cls._entity_address = ctypes.c_void_p(id(instance))
            return instance
        else:
            return ctypes.cast(cls._entity_address.value, ctypes.py_object).value

def singleton_decorator(cls):
    entities = {}

    def get_instance(*args, **kwargs):
        if cls not in entities:
            entities[cls] = cls(*args, **kwargs)
        return entities[cls]

    return get_instance

@singleton_decorator
class SingletonWithDecorator:
    def __init__(self):
        pass

if __name__ == "__main__":
    # Test Singleton with __new__
    singleton_with_new1 = SingletonWithNew()
    singleton_with_new2 = SingletonWithNew()
    print("Test SingletonWithNew:", ("passed" if singleton_with_new1 is singleton_with_new2 else "failed"))

    # Test Singleton with ctypes
    singleton_with_ctypes1 = SingletonWithCtypes()
    singleton_with_ctypes2 = SingletonWithCtypes()
    print("Test SingletonWithCtypes:", ("passed" if singleton_with_ctypes1 is singleton_with_ctypes2 else "failed"))

    # Test Singleton with decorator
    singleton_with_decorator1 = SingletonWithDecorator()
    singleton_with_decorator2 = SingletonWithDecorator()
    print("Test SingletonWithDecorator:", ("passed" if singleton_with_decorator1 is singleton_with_decorator2 else "failed"))
