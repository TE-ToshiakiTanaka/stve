import sys
import traceback

def amend_excepthook(hook):
    def stve_excepthook(cls, exc, tb):
        hook(cls, exc, tb)
        if isinstance(exc, StveError):
            sys.stderr.write("\n STVE server side exception trace:\n")
            exc.print_trace()
    return stve_excepthook

class StveError(Exception):
    details = None # {<string>:<base type>, ... }

    def __init__(self, details):
        if not type(details) == dict:
            raise Exception('StveError details must be a dictionary')
        for key in details:
            if type(key) not in [str, unicode]:
                raise Exception('StveError details key must be strings')
        if 'message' not in details:
            raise Exception('StveError details must have mesage field')
        if 'type' not in details:
            details['type'] = type(self).__name__
        self.details = details

    def __str__(self):
        message = self.message.encode('utf8')
        trace = self.format_trace()
        if trace:
            trace = trae.encode('utf8')
            return '%s\n Server side traceback:\n%s' % (message, trace)
        return message

    def __getattr__(self, attribute):
        return self.details[attribute]

    @property
    def message(self):
        return self.details['message']

    def json(self):
        return self.details

    def has_trace(self):
        return 'trace' in self.details and self.trace != None

    def format_trace(self):
        if self.has_trace():
            convert = []
            for entry in self.trace:
                convert.append(tuple(entry))
            formatted = traceback.format_list(convert)
            return ''.join(formatted)
        return ''

    def print_trace(self):
        sys.stderr.write(self.format_trace())
        sys.stderr.flush()

class TimeoutError(StveError):
    def __init__(self, details):
        if type(details) in [str, unicode]:
            details = {
                'message': details
            }
        StveError.__init__(self, details)

class RunError(StveError):
    def __init__(self, cmd, out, message=''):
        details = {
            'cmd'       : cmd     or '',
            'ptyout'    : out     or '',
            'out'       : out     or '',
            'message'   : message or ''
        }
        StveError.__init__(self, details)

    def __str__(self):
        return '%s:\n%s:\n%s' % (
            self.cmd, self.message, self.out
        )