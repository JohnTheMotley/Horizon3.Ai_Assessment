from flask import Flask, request
import sys
import json
from lib.csv_manager import CsvManager


# application accepts a csv file to query against as a command-line argument
try:
    assert len(sys.argv) == 3
except:
    print('Usage: main.py <port> <csv_filepath>')
    sys.exit(1)

try:
    port = (int)(sys.argv[1])
except:
    print('Error loading PORT argument')
    sys.exit(1)

try:
    csv_data = CsvManager(sys.argv[2])
except:
    print('Error loading CSV_FILEPATH argument')
    sys.exit(1)

        
app = Flask(__name__)
app.config['DEBUG'] = False

# A single endpoint for the assessment's api
@app.route('/', methods=['GET'])
def query_api():
    # shouldn't need sanitization, just accessing dicts and sets based on these
    ip = request.args.get('ip')
    protocol = request.args.get('protocol')
    port = request.args.get('port')
    # returns a set, so convert to list before the json serialization
    return json.dumps(list(csv_data.query(ip, protocol, port)))

# flask doesn't provide a production-quality webserver by itself
if __name__ == "__main__":
    from waitress import serve
    serve(app, port=port)