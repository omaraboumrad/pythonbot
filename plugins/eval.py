from helpers import msg


@msg('eval (?P<code>.*)')
def handle(bot, grouper):
    who = grouper('nick')
    target = grouper('target')
    try:
        result = str(eval(grouper('code')))
    except Exception as e:
        result = str(e)

    bot.privmsg(target, '{}: {}'.format(who, result))
