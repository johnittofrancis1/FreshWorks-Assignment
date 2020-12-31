import json
import os
from datetime import datetime, date
import sys
import threading


class DataStore:
    """
    DataStore class for methods to handle CRD (Create, Read, Delete) operations in a file-based datastore
    """

    __instance = None

    def __init__(self, file_path):
        if DataStore.__instance is not None:
            raise Exception("This is a Singleton Class!")
        else:
            DataStore.__instance = self
            self._file_path = file_path
            self._global_lock = threading.Lock()
            if not os.path.exists(self._file_path):
                with open(self._file_path, "w") as f:
                    json.dump({"created": date.today().strftime("%d/%m/%Y")}, f, indent=4)

    @staticmethod
    def connect(file_path=os.getcwd()+"\\db.json"):
        """
        Connects to a file datastore
            :parameter
            file_path: String, optional
                File Path for the datastore
            :returns
            instance of the DataStore class
        """
        if DataStore.__instance is None:
            DataStore(file_path)
        return DataStore.__instance

    def create(self, key, value, time_to_live=-1):
        """
        Creates a key-value pair in the datastore with optional time-to-live feature
            :parameter
            key: String,
            value: JSON object,
            time_to_live: integer, optional
                seconds in integer
            :returns
            None
        """
        while self._global_lock.locked():
            continue
        v = {"val": value}
        json_size = sys.getsizeof(json.dumps(v))
        if json_size > 16 * 1024:
            raise ValueExceedingException("The value exceeds 16 KB")
        if len(key) > 32:
            key = key[:30] + ".."
        if (json_size + os.path.getsize(self._file_path)) > 1 * 1024 * 1024 * 1024:
            raise Exception("The file size exceeds 1 GB")
        if time_to_live > 0:
            v["expiry"] = round(datetime.now().timestamp()) + time_to_live
        else:
            v["expiry"] = -1
        self._global_lock.acquire()
        with open(self._file_path, "r") as f:
            data = json.load(f)
            if key in data:
                raise KeyExistsException("This key \""+key+"\" already exists")
            else:
                data.update({key: v})
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=4)
        self._global_lock.release()

    def read(self, key):
        """
        Gives a value given a key that is already stored in the datastore
            :parameter
            key: String
            :returns
            JSON object
        """
        while self._global_lock.locked():
            continue
        self._global_lock.acquire()
        ans = None
        with open(self._file_path, "r") as f:
            data = json.load(f)
            v = data.get(key, None)
            if v is None:
                raise KeyNotFoundException("There is no such key \'"+key+"\'")
            else:
                if key == "created":
                    ans = v
                else:
                    exp = v.get("expiry", -1)
                    if exp <= 0 or exp >= round(datetime.now().timestamp()):
                        ans = v.get("val", None)
                    else:
                        del data[key]
                        with open(self._file_path, "w") as f:
                            json.dump(data, f, indent=4)
                        raise KeyNotFoundException("There is no such key \'"+key+"\'")
        self._global_lock.release()
        return ans

    def delete(self, key):
        """
        Deletes a key-value pair given a key that is already stored in the datastore
            :parameter
            key: String
            :returns
            JSON object: deleted key-value pair
        """
        while self._global_lock.locked():
            continue
        self._global_lock.acquire()
        with open(self._file_path, "r") as f:
            data = json.load(f)
            v = data.get(key, None)
            if v is None:
                raise KeyNotFoundException("There is no such key \'"+key+"\'")
            else:
                exp = v.get("expiry", -1)
                if exp <= 0 or exp >= round(datetime.now().timestamp()):
                    resp = v["val"]
                    del data[key]
                else:
                    del data[key]
                    raise KeyNotFoundException("There is no such key \'"+key+"\'")
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=4)
        self._global_lock.release()
        return resp


class ValueExceedingException(Exception):

    def __init__(self, message):
        self.message = message


class KeyNotFoundException(Exception):

    def __init__(self, message):
        self.message = message


class KeyExistsException(Exception):

    def __init__(self, message):
        self.message = message
