import os


class Config:
    """class for enviroment variables"""

    __env__ = os.environ.copy()

    def __getstate__(self):
        print("config1--2")
        return vars(self)

    def __setstate__(self, state):
        vars(self).update(state)

    def __getattribute__(self, name: str) -> str:
        """get attribute from env parameters class or module"""
        try:
            return super().__getattribute__(name)
        except AttributeError:
            name = name.upper()
            return self.__env__.get(name)

    def __setattr__(self, name, value):
        """get attribute from env parameters class or module"""
        try:
            value = super().__getattribute__(name)
            raise AttributeError("Readonly Attribute")
        except AttributeError:
            name = name.upper()
            self.__env__[name] = value

    def get(self, name):
        return self.__getattribute__(name)

    def must_get(self, name):
        """raise exception if var is None"""
        var = self.__getattribute__(name)
        if not var:
            raise TypeError
        return var


config = Config()


def need(param, default=None, required=False, into=None) -> None:
    current = config.get(param)
    if current:
        if into:
            config.__setattr__(param, into(current))
        return
    if default:
        if into:
            if isinstance(default, into):
                config.__setattr__(param, default)
                return
            raise TypeError
        config.__setattr__(param, default)
        return
    if required:
        raise AttributeError(f"Missing env parameter : {param.upper()}")
    else:
        config.__setattr__(param, None)
        return


need("ENVIRONMENT", required=True)
