import argparse

from app.acceptor import app
from app.rest_api import api, configure_rest_api
from app.configuration.configuration_factory import ConfigurationFactory

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--environment', type=str, help="docker/dev", required=True)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    configuration = ConfigurationFactory.createConfiguration(args.environment)
    configure_rest_api(api, configuration)
    app.run(
        host=configuration.host,
        port=configuration.port,
        debug=configuration.debug,
        use_debugger=configuration.use_debugger,
        use_reloader=configuration.use_reloader)