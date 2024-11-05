# Base class for a hash table that supports the insert, remove, and search 
# operations.
class HashTable:
    # Returns a non-negative hash code for the specified key.
    def hashKey(self, key):
        return abs(hash(key))
    
    # Inserts the specified key/value pair. If the key already exists, the 
    # corresponding value is updated. If inserted or updated, True is returned. 
    # If not inserted, then False is returned.
    def insert(self, key, value):
        pass
    
    # Searches for the specified key. If found, the key/value pair is removed 
    # from the hash table and True is returned. If not found, False is returned.
    def remove(self, key):
        pass
    
    # Searches for the key, returning the corresponding value if found, None if 
    # not found.
    def search(self, key):
        pass

## Chaining Hash Table

class ChainingHashTableItem:
    def __init__(self, itemKey, itemValue):
        self.key = itemKey
        self.value = itemValue
        self.next = None

class ChainingHashTable(HashTable):
    def __init__(self, initialCapacity = 11):
        self.table = [None] * initialCapacity

    # Inserts the specified key/value pair. If the key already exists, the 
    # corresponding value is updated. If inserted or updated, True is returned. 
    # If not inserted, then False is returned.    
    def insert(self, key, value):
        # Hash the key to get the bucket index
        bucket_index = self.hashKey(key) % len(self.table)
      
        # Traverse the linked list, searching for the key. If the key exists in 
        # an item, the value is replaced. Otherwise a new item is appended.
        item = self.table[bucket_index]
        previous = None
        while item != None:
            if key == item.key:
                item.value = value
                return True
            
            previous = item
            item = item.next
      
        # Append to the linked list
        if self.table[bucket_index] == None:
            self.table[bucket_index] = ChainingHashTableItem(key, value)
        else:
            previous.next = ChainingHashTableItem(key, value)
        return True

    # Searches for the specified key. If found, the key/value pair is removed 
    # from the hash table and True is returned. If not found, False is returned.    
    def remove(self, key):
        # Hash the key to get the bucket index
        bucket_index = self.hashKey(key) % len(self.table)
        
        # Search the bucket's linked list for the key
        item = self.table[bucket_index]
        previous = None
        while item != None:
            if key == item.key:
                if previous == None:
                    # Remove linked list's first item
                    self.table[bucket_index] = item.next
                else:
                    previous.next = item.next
                return True
            previous = item
            item = item.next
        return False # key not found
   
    # Searches for the key, returning the corresponding value if found, None if 
    # not found.
    def search(self, key):
        # Hash the key to get the bucket index
        bucket_index = self.hashKey(key) % len(self.table)
        
        # Search the bucket's linked list for the key
        item = self.table[bucket_index]
        while item != None:
            if key == item.key:
                return item.value
            item = item.next
        return None # key not found
   
    def __str__(self):
        result = ""
        for i in range(len(self.table)):
            result += "%d: " % i
            if self.table[i]== None:
                result += "(empty)\n"
            else:
                item = self.table[i]
                while item != None:
                    result += "%s, %s --> " % (str(item.key), str(item.value))
                    item = item.next
                result += "\n"
        return result

## Open Addressing Bucket

# OpenAddressingBucket represents a bucket with a key and a value
class OpenAddressingBucket:
    def __init__(self, bucket_key = None, bucket_value = None):
        self.key = bucket_key
        self.value = bucket_value
    
    def isEmpty(self):
        if self is OpenAddressingBucket.EMPTY_SINCE_START:
            return True
        return self is OpenAddressingBucket.EMPTY_AFTER_REMOVAL

# Initialize two special bucket types: empty-since-start and empty-after-removal
OpenAddressingBucket.EMPTY_SINCE_START = OpenAddressingBucket()
OpenAddressingBucket.EMPTY_AFTER_REMOVAL = OpenAddressingBucket()

# OpenAddressingHashTable is a base class for an open addressing hash table
class OpenAddressingHashTable(HashTable):
    def __init__(self, initialCapacity):
        self.table = [OpenAddressingBucket.EMPTY_SINCE_START] * initialCapacity
    
    def probe(self, key, i):
        # Each derived class must implement
        pass

    # Inserts the specified key/value pair. If the key already exists, the 
    # corresponding value is updated. If inserted or updated, True is returned. 
    # If not inserted, then False is returned.   
    def insert(self, key, value):
        # Search for the key in the table. If found, update the bucket's value.
        for i in range(len(self.table)):
            bucket_index = self.probe(key, i)
            
            # An empty-since-start bucket implies the key is not in the table
            if self.table[bucket_index] is OpenAddressingBucket.EMPTY_SINCE_START:
                break
            
            if self.table[bucket_index] is not OpenAddressingBucket.EMPTY_AFTER_REMOVAL:
                # Check if the non-empty bucket has the key
                if key == self.table[bucket_index].key:
                    # Update the value
                    self.table[bucket_index].value = value
                    return True
        
        # The key is not in the table, so insert into first empty bucket
        for i in range(len(self.table)):
            bucket_index = self.probe(key, i)
            if self.table[bucket_index].isEmpty():
                self.table[bucket_index] = OpenAddressingBucket(key, value)
                return True
        
        return False # no empty bucket found

    # Searches for the specified key. If found, the key/value pair is removed 
    # from the hash table and True is returned. If not found, False is returned.   
    def remove(self, key):
        for i in range(len(self.table)):
            bucket_index = self.probe(key, i)
            
            # An empty-since-start bucket implies the key is not in the table
            if self.table[bucket_index] is OpenAddressingBucket.EMPTY_SINCE_START:
                return False
            
            if self.table[bucket_index] is not OpenAddressingBucket.EMPTY_AFTER_REMOVAL:
                # Check if the non-empty bucket has the key
                if key == self.table[bucket_index].key:
                   # Remove by setting the bucket to empty-after-removal
                   self.table[bucket_index] = OpenAddressingBucket.EMPTY_AFTER_REMOVAL
                   return True
        return False # key not found
   
    # Searches for the key, returning the corresponding value if found, null if 
    # not found.
    def search(self, key):
        for i in range(len(self.table)):
            bucket_index = self.probe(key, i)
            
            # An empty-since-start bucket implies the key is not in the table
            if self.table[bucket_index] is OpenAddressingBucket.EMPTY_SINCE_START:
                return None
            
            if self.table[bucket_index] is not OpenAddressingBucket.EMPTY_AFTER_REMOVAL:
                # Check if the non-empty bucket has the key
                if key == self.table[bucket_index].key:
                    return self.table[bucket_index].value
        
        return None # key not found
   
    def __str__(self):
        result = ""
        for i in range(len(self.table)):
            result += "%d: " % i
            if self.table[i] is OpenAddressingBucket.EMPTY_SINCE_START:
                result += "EMPTY_SINCE_START\n"
            elif self.table[i] is OpenAddressingBucket.EMPTY_AFTER_REMOVAL:
                result += "EMPTY_AFTER_REMOVAL\n"
            else:
                result += "%s, %s\n" % (self.table[i].key, self.table[i].value)
        return result

## Linear Probing

class LinearProbingHashTable(OpenAddressingHashTable):
    def __init__(self, initial_capacity = 11):
        OpenAddressingHashTable.__init__(self, initial_capacity)
    
    # Returns the bucket index for the specified key and i value using the 
    # linear probing sequence.
    def probe(self, key, i):
        return (self.hashKey(key) + i) % len(self.table)

## Quadratic Probing

class QuadraticProbingHashTable(OpenAddressingHashTable):
    def __init__(self, c1 = 1, c2 = 1, initial_capacity = 11):
        OpenAddressingHashTable.__init__(self, initial_capacity)
        self.c1 = c1
        self.c2 = c2
    
    # Returns the bucket index for the specified key and i value using the 
    # quadratic probing sequence.
    def probe(self, key, i):
        return (self.hashKey(key) + self.c1 * i + self.c2 * i * i) % len(self.table)

## Double Hashing

class DoubleHashingHashTable(OpenAddressingHashTable):
    def __init__(self, initial_capacity = 11):
        OpenAddressingHashTable.__init__(self, initial_capacity)
    
    def h2(self, key):
        return 7 - self.hashKey(key) % 7
    
    # Returns the bucket index for the specified key and i value using the 
    # double hashing probing sequence.
    def probe(self, key, i):
        return (self.hashKey(key) + i * self.h2(key)) % len(self.table)

