from helpers import raw


@raw('^PING :(?P<who>.*)')
def handle(bot, grouper):
    server = grouper('who')
    bot.send_raw('PONG {}\n'.format(server))
