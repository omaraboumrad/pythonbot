import json
import time
import urllib2

from helpers import msg


@msg('hn (?P<count>\d+)')
def handle(bot, grouper):
    target = grouper('target')
    count = int(grouper('count'))

    f = urllib2.urlopen('http://api.hackernews.com/page')
    response = f.read()
    f.close()

    if not response:
        bot.privmsg(target, 'Not found')
    else:
        d = json.loads(response)
        delivered = 0
        for entry in d['items']:
            time.sleep(1)
            bot.privmsg(target, '{} - {}'.format(
                entry['title'].encode('utf-8'),
                entry['url'].encode('utf-8')))
            delivered += 1
            if delivered >= count:
                break
