import datetime
import json
import os
import threading
import time
from unittest import TestCase
from . import DataStore, ValueExceedingException, KeyExistsException, KeyNotFoundException


class TestDataStore(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_path = os.getcwd()+"\\db_test.json"
        if os.path.exists(self._file_path):
            os.remove(self._file_path)

    def test_connect(self):
        d = DataStore.connect(self._file_path)
        self.assertTrue(os.path.exists(self._file_path), "DataStore file connection doesn't work")

    def test_create(self):
        d = DataStore.connect(self._file_path)
        k, v = "dict", {"name": "Johnitto Francis", "rollno": 1234}
        d.create(k, v)
        self.assertTrue(self.read_check(d, k, v), "Key is not created properly")

    def test_read(self):
        d = DataStore.connect(self._file_path)
        k, v = "created", datetime.date.today().strftime("%d/%m/%Y")
        self.assertTrue(self.read_check(d, k, v), "Key is not found")

    def test_delete(self):
        d = DataStore.connect(self._file_path)
        k, v = "delete", "create to delete"
        d.create(k, v)
        self.assertEqual(d.delete(k), v, "Delete operation doesn't work")

    def test_default_file_create(self):
        d = DataStore.connect()
        self.assertTrue(d._file_path, "Default DataStore file connection doesn't work")

    def test_key_capping(self):
        d = DataStore.connect(self._file_path)
        k, v = "".join(["k" for _ in range(36)]), "Key capped at 36 chars"
        d.create(k, v)
        self.assertEqual(d.read(k[:30]+".."), v, "The key is not capped at 36 chars")

    def test_value_limit(self):
        d = DataStore.connect(self._file_path)
        with open(os.getcwd()+"\\ds\\test_json.json", "r") as f:
            k, v = ">16KB", json.load(f)
        self.assertRaises(ValueExceedingException, d.create, k, v)

    def test_time_to_live(self):
        d = DataStore.connect()
        k, v = "timeToLive", "5sec"
        d.create(k, v, time_to_live=1)
        time.sleep(2)
        self.assertRaises(KeyNotFoundException, d.read, k)

    @staticmethod
    def read_check(d, k, v):
        return d.read(k) == v


def create_and_run_thread(no_threads):
    d = DataStore.connect()
    threads = [threading.Thread(target=thread_function, args=(str(i), d)) for i in range(no_threads)]
    for t in threads:
        t.start()
        t.join()


def thread_function(name, d):
    k = "".join([name for _ in range(37)])
    print("Thread "+name+" connected to the Datastore")
    d.create(k, "john")
    print("Thread "+name+" created a key")


def test_thread_safe():
    try:
        create_and_run_thread(5)
    except Exception:
        print("DataStore is not thread-safe")
