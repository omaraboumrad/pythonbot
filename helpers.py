def raw(pattern):
    def plug_around(action):
        action.pattern = pattern
        return action
    return plug_around


def msg(pattern):
    prefix = '^:(?P<nick>.*)!(?P<name>.*)@(?P<ip>.*) PRIVMSG (?P<target>.*) :'

    def plug_around(action):
        action.pattern = prefix + pattern
        return action
    return plug_around
