from time import gmtime, strftime


def log(message):
	time = strftime("%H:%M:%S | %m.%d", gmtime())
	print("{time}: \t {message}".format(time=time, message=message))
