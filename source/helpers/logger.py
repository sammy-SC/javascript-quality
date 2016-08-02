from time import gmtime, strftime


def log(message):
    '''
    logs a message with time into standard output
    '''
    assert message is not None
    time = strftime("%H:%M:%S | %m.%d", gmtime())
    print("{time}: \t {message}".format(time=time, message=message))
