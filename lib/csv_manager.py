import csv, json

class Entry(dict):
    def __init__(self, ip: str, protocol: str, port: str):
        self.ip = ip
        self.protocol = protocol
        self.port = port
        # This line is to make json serialization easier
        # Mainly prevents having to write a custom serializer and include it in dumps calls
        # port=(int) is a hacky solution so I don't have to parse all incoming port queries to int
        # just to return ports as an int. In a real environment I'd fix that.
        dict.__init__(self, ip=self.ip, protocol=self.protocol, port=(int)(port))
    
    # Used to work with entries in sets as unique items
    def __hash__(self):
        return hash((self.ip, self.protocol, self.port))
    
    # Has to be implemented or __hash__ is ignored
    # https://docs.python.org/3/reference/datamodel.html#object.__hash__
    def __eq__(self, other):
        return self.ip == other.ip and self.protocol == other.protocol and self.port == other.port

class CsvManager:
    def __init__(self, csv_filename: str):
        self.all_entries = set()
        self.by_ip = {}
        self.by_protocol = {}
        self.by_port = {}

        self.load(csv_filename)
    
    # More fun than just loading into a database, potentially more efficient in this usecase
    # We track entries by sets of unique entries by field value
    def add(self, entry: Entry):
        if entry not in self.all_entries:
            self.all_entries.add(entry)
        
        if entry.ip not in self.by_ip:
            self.by_ip[entry.ip] = set()
        self.by_ip[entry.ip].add(entry)

        if entry.protocol not in self.by_protocol:
            self.by_protocol[entry.protocol] = set()
        self.by_protocol[entry.protocol].add(entry)

        if entry.port not in self.by_port:
            self.by_port[entry.port] = set()
        self.by_port[entry.port].add(entry)

    # The set logic allows us to easily combine (AND) on query params
    def query(self, ip: str, protocol: str, port: str):
        to_ret = self.all_entries

        if ip:
            if ip not in self.by_ip:
                return set()
            to_ret = to_ret.intersection(self.by_ip[ip])
        
        if protocol:
            if protocol not in self.by_protocol:
                return set()
            to_ret = to_ret.intersection(self.by_protocol[protocol])
        
        if port:
            if port not in self.by_port:
                return set()
            to_ret = to_ret.intersection(self.by_port[port])
        
        return to_ret
    
    def load(self, csv_filename):
        with open(csv_filename) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                entry = Entry(row[0], row[1], row[2])
                self.add(entry)