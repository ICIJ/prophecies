class ExtendedNamespace:

    @staticmethod
    def map_key_value(value):
        if isinstance(value, dict):
            return ExtendedNamespace(value)
        return value

    def __init__(self, dict_or_list):
        if type(dict_or_list) == dict:
            for key, value in dict_or_list.items():
                if type(value) == dict:
                    setattr(self, key, ExtendedNamespace(value))
                elif type(value) == list:
                    setattr(self, key, list(map(self.map_key_value, value)))
                else:
                    setattr(self, key, value)
        elif type(dict_or_list) == list:
            setattr(self, '__list__', list(map(self.map_key_value, dict_or_list)))

    def __getitem__(self, attr):
        if type(attr) == int:
            return self.__list__[attr]
        return getattr(self, attr)
