# Python version: 3.11.2

import argparse

from scripts.app import App
from scripts.net.client import NetClient
from scripts.net.server import run as run_server


def parse_args():
    parser = argparse.ArgumentParser(description="Empty Pygame Project")
    parser.add_argument("--server", action="store_true", help="run the game server")
    parser.add_argument("--connect", metavar="HOST:PORT", help="join a server (ex. 127.0.0.1:5000)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.server:
        run_server()
    elif args.connect:
        host, port = args.connect.rsplit(":", 1)
        app = App(client=NetClient(host, int(port)))
    else:
        app = App()

    while True:
        app.update()
