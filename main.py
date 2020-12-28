import json
import os
from datetime import datetime, date


class DataStore:

    __instance = None

    def __init__(self, file_path):
        if DataStore.__instance is not None:
            raise Exception("This is a Singleton Class!")
        else:
            DataStore.__instance = self
            self._file_path = file_path
            if not os.path.exists(self._file_path):
                with open(self._file_path, "w") as f:
                    json.dump({"created": date.today().strftime("%d/%m/%Y")}, f, indent=4)

    @staticmethod
    def connect(file_path=os.getcwd()+"\db.json"):
        if DataStore.__instance is None:
            DataStore(file_path)
        return DataStore.__instance

    def create(self, key, value, time_to_live=-1):
        v = dict()
        v["val"] = value
        if time_to_live > 0:
            v["expiry"] = round(datetime.now().timestamp()) + time_to_live
        else:
            v["expiry"] = -1
        with open(self._file_path, "r") as f:
            data = json.load(f)
            if key in data:
                raise Exception("This key \""+key+"\" already exists")
            else:
                data.update({key: v})
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=4)

    def read(self, key):
        with open(self._file_path, "r") as f:
            data = json.load(f)
            v = data.get(key, None)
            if v is not None:
                if v.get("expiry", -1) >= round(datetime.now().timestamp()):
                    return v.get("val", None)
                elif v.get("expiry", -1) < 0:
                    return v.get("val", None)
                else:
                    del data[key]
                    with open(self._file_path, "w") as f:
                        json.dump(data, f, indent=4)
            else:
                return None

    def delete(self, key):
        with open(self._file_path, "r") as f:
            data = json.load(f)
            resp = data[key]
            del data[key]
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=4)
        return resp


d = DataStore.connect(os.path.join(os.getcwd(), "sdb.json"))
# cmd = input()
# while cmd != "exit":
#     if cmd[0] == "C":
#         c, k, v = cmd.split()
#         d.create(k, v)
#     elif cmd[0] == "R":
#         c, k = cmd.split()
#         print(d.read(k))
#     elif cmd[0] == "D":
#         c, k = cmd.split()
#         print(d.delete(k))
#     cmd = input()
c = {"john": {"id": 123, "name": "Johnitto Francis"}, "joan": {"id": 12}}
# d.create("johnitto", "francis", time_to_live=100)
print(d.read("johnitto"))
print(datetime.now().timestamp())
