import re

from helpers import msg

counter = {}


@msg('(?P<text>.*)')
def handle(bot, grouper):
    words = ['C++', 'Java', 'Python', 'Haskell']
    target = grouper('target')
    text = grouper('text')
    caught = []
    for word in words:
        total = len(re.findall(re.escape(word), text))
        if total:
            counter[word] = counter.get(word, 0) + total
            caught.append((word, counter[word]))

    if caught:
        message = '{} has been mentioned {} time(s)'
        friendly = ', '.join(message.format(a, b) for a, b in caught)
        bot.privmsg(target, friendly)
