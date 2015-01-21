#!/usr/bin/env python

from flask.ext.script import Manager, Server
from app import app, socketio

manager = Manager(app)
manager.add_command("runserver",Server())

if __name__ == "__main__":
    #manager.run()
    socketio.run(app)
