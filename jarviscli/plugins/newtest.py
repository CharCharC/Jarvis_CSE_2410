from plugin import plugin


@plugin('newtest')
def newtest(jarvis, s):

    jarvis.say("hello this is a test")
