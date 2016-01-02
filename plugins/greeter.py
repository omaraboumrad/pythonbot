from helpers import msg


@msg('(hi|hello|howdy|hey|good morning)')
def handle(bot, grouper):
    print grouper
    who = grouper('nick')
    target = grouper('target')
    bot.privmsg(target, 'Hello {}!'.format(who))
