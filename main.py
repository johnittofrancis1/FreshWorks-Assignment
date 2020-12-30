import json
import os
import sys

from ds import DataStore

# d = DataStore.connect((os.path.join(os.getcwd(), "db.json")))
# cmd = input()
# while cmd != "exit":
#     try:
#         if cmd[0] == "C":
#             c, k, v, t = cmd.split()
#             d.create(k, v, int(t))
#         elif cmd[0] == "R":
#             c, k, = cmd.split()
#             print(d.read(k))
#         elif cmd[0] == "D":
#             c, k, = cmd.split()
#             print(d.delete(k))
#     except Exception as e:
#         print(e)
#     finally:
#         cmd = input()

with open(os.getcwd()+"\\ds\\test_json.json", "r") as f:
    j = json.load(f)
    print(sys.getsizeof(j))
    d = DataStore.connect()
    d.create("j", j)
