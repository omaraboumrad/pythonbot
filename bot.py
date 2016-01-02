#! /usr/bin/env python
import ConfigParser
import functools
import glob
import imp
import os
import re
import select
import socket
import sys


class Bot(object):

    def __init__(self, host, port, details, channels):
        self.host = host
        self.port = port
        self.details = details
        self.channels = channels
        self.plugins = self.load_plugins()

    def load_plugins(self):
        plugins = []
        files = glob.glob(os.path.join(os.path.dirname(__file__),
                                       'plugins', '*.py'))

        for f in files:
            module = os.path.basename(f)[:-3]
            print("Found Plugin: {} ".format(module))
            plugin = imp.load_module(module,
                                     *imp.find_module(module, ['plugins']))
            plugins.append(plugin)

        return plugins

    @classmethod
    def from_config(cls, filename):
        parser = ConfigParser.RawConfigParser()
        parser.read(filename)
        config = functools.partial(parser.get, 'Config')
        return cls(
            details=dict(
                nickname=config('nickname'),
                realname=config('realname'),
                hostname=config('hostname'),
                servername=config('servername'),
                username=config('username')),
            channels=config('channels').split(),
            host=config('host'),
            port=int(config('port')),
        )

    def handle(self, line):
        for module in self.plugins:
            match = re.search(module.handle.pattern, line)
            if match:
                print('>>> Matched: {}'.format(module.handle.pattern))
                module.handle(self, match.group)

    def register(self):
        buf = ['USER {} {} {} {}\n'.format(self.details['username'],
                                           self.details['hostname'],
                                           self.details['servername'],
                                           self.details['realname']),
               'NICK {}\n'.format(self.details['nickname'])]
        self.send_raw(''.join(buf))

    def auto_join(self):
        for channel in self.channels:
            self.client.sendall('JOIN #{}\n'.format(channel))

    def send_raw(self, message):
        self.client.sendall(message)

    def privmsg(self, target, message):
        self.client.sendall('PRIVMSG {} :{}\n'.format(target, message))

    def connect(self):
        self.client = socket.socket()
        self.client.connect((self.host, int(self.port)))

        self.register()
        self.auto_join()

        while True:
            seed = ''
            readable, _, _ = select.select([self.client, sys.stdin], [], [])
            for reader in readable:
                if reader == self.client:
                    data = self.client.recv(4096)
                    lines = [line for line in (seed+data).split('\n')]
                    seed = lines.pop()
                    for line in lines:
                        print(line)
                        self.handle(line)
                elif reader == sys.stdin:
                    message = sys.stdin.readline().strip('\n')
                    for channel in self.channels:
                            self.privmsg(channel, message)


if __name__ == '__main__':
    bot_ = Bot.from_config('bot.ini')
    bot_.connect()
