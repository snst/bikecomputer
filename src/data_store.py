from setting_val import *
import data_global as g

class DataStore:
    def save(self, filename):
        config = {}
        attr = self.get_all_attributes()
        for a in attr:
            val = getattr(self, a, None)
            if type(val) is SettingVal:
                config[a] = val.value
        try:
            f = open(filename, 'w')
            f.write(g.hal.json_dump(config))
            f.close()
        except Exception as e:
            print(e)
            pass

    def get_all_attributes(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def load(self, filename):
        try:
            with open(filename) as fp:
                config = g.hal.json_load(fp.read())
                for key, val in config.items():
                    attr = getattr(self, key, None)
                    if attr:
                        attr.value = val
        except Exception as e:
            print(e)
            pass
        pass
