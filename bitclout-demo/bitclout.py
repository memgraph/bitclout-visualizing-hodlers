import database
import json
import logging
import mgclient
import os
import time
from argparse import ArgumentParser
from flask import Flask, render_template, Response

MG_HOST = os.getenv('MG_HOST', '127.0.0.1')
MG_PORT = int(os.getenv('MG_PORT', '7687'))

log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.INFO)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


init_log()


def parse_args():
    '''
    Parse command line arguments.
    '''
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--app-host", default="0.0.0.0",
                        help="Host address.")
    parser.add_argument("--app-port", default=5000, type=int,
                        help="App port.")
    parser.add_argument("--template-folder", default="public/template",
                        help="Path to the directory with flask templates.")
    parser.add_argument("--static-folder", default="public",
                        help="Path to the directory with flask static files.")
    parser.add_argument("--debug", default=True, action="store_true",
                        help="Run web server in debug mode.")
    parser.add_argument("--load-data", default=False, action='store_true',
                        help="Load BitClout network into Memgraph.")
    print(__doc__)
    return parser.parse_args()


args = parse_args()

connection_established = False
while(not connection_established):
    try:
        connection = mgclient.connect(
            host=MG_HOST,
            port=MG_PORT,
            username="",
            password="",
            sslmode=mgclient.MG_SSLMODE_DISABLE,
            lazy=True)
        connection_established = True
    except:
        log.info("Memgraph probably isn't running.")
    time.sleep(4)

cursor = connection.cursor()

app = Flask(__name__,
            template_folder=args.template_folder,
            static_folder=args.static_folder,
            static_url_path='')


@app.route('/load-all', methods=['GET'])
def load_all():
    """Load everything from the database."""

    start_time = time.time()
    try:
        cursor.execute("""MATCH (n)-[r]-(m)
                                    RETURN n, r, m
                                    LIMIT 10000;""")
        rows = cursor.fetchall()
    except:
        log.info("Something went wrong.")
        return ('', 204)

    links = []
    nodes = []
    visited = []

    for row in rows:
        n = row[0]
        m = row[2]
        if n.id not in visited:
            nodes.append({'id': n.id})
            visited.append(n.id)
        if m.id not in visited:
            nodes.append({'id': m.id})
            visited.append(m.id)
        links.append({'source': n.id, 'target': m.id})

    response = {'nodes': nodes, 'links': links}

    duration = time.time() - start_time
    log.info("Data fetched in: " + str(duration) + " seconds")

    return Response(
        json.dumps(response),
        status=200,
        mimetype='application/json')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def main():
    if args.load_data:
        log.info("Loading the data into Memgraph.")
        database.load_data(cursor)

    app.run(host=args.app_host, port=args.app_port, debug=args.debug)


if __name__ == "__main__":
    main()
