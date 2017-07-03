from time import strftime, localtime

class HTMLtime:
    def get_dirtime(self):
        time = strftime("%H-%M-%S", localtime())
        return time

    def get_time(self):
        h = strftime("%H", localtime())
        m = strftime("%M", localtime())
        s = strftime("%S", localtime())
        time = h + " h " + m + " m " + s +" s"
        return time

    def get_dirday(self):
        day = strftime("%Y-%m-%d", localtime())
        return day