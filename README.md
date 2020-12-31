A package to handle CRD operations in a File-based Key Value DataStore

Example in action
```
from ds import DataStore

# connecting to a datastore file
d = DataStore.connect("C:\\Users\\johni\\Desktop\\db.json")

# creating a key-value pair
d.create("key", "value", time_to_live=30)

# reading the value by giving a key
print(d.read("key"))

# deleting the key-value pair
d.delete("key")
```
