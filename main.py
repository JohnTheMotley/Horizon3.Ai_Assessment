from flask import Flask, request
import sys
import json
from lib.csv_manager import CsvManager


# application accepts a csv file to query against as a command-line argument
assert len(sys.argv) == 2

try:
    csv_data = CsvManager(sys.argv[1])
except:
    print('Error loading csv data....')
    sys.exit(1)

        
app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/', methods=['GET'])
def query_api():
    ip = request.args.get('ip')
    protocol = request.args.get('protocol')
    port = request.args.get('port')
    return json.dumps(list(csv_data.query(ip, protocol, port)))

app.run()