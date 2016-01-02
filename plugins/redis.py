import subprocess

from helpers import msg


@msg('r (?P<cmd>.*)')
def handle(bot, grouper):
    who = grouper('nick')
    target = grouper('target')
    try:
        ps = subprocess.Popen(['redis-cli']+grouper('cmd').split(),
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE)
        (stdout, stderr) = ps.communicate()

        result = str(stdout)
    except Exception as e:
        result = str(e)

    bot.privmsg(target, '{}: [REDIS] {}'.format(who, result))
