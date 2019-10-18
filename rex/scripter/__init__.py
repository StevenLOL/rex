"""
Module to make script generation customizable
"""
import string

import jinja2


env = jinja2.Environment(
    loader=jinja2.PackageLoader('rex', 'scripter/templates'),
    trim_blocks=True)

def cstring(b):
    assert type(b) is bytes
    printable = set(map(ord, (string.ascii_letters +
                              string.digits +
                              string.punctuation +
                              ' ')))
    printable -= set(map(ord, '\\"'))
    result = ''.join(chr(i) if i in printable else ('\\' + oct(i)[2:].rjust(3, '0'))
                     for i in b)
    return '"' + result + '"'

env.filters['cstring'] = cstring


class Scripter:
    """
    A scripter object is the abstraction of exploit generation.
    It is used to generate standalone exploits according to user provided specifications
    """


    def __init__(self, template='python', arguments=None, **kwargs):
        if arguments is None:
            arguments = []
        self._template = env.get_template(template + '.j2')
        self._arguments = arguments
        self._kwargs = kwargs
        self._actions = []

    def recv(self, n):
        self._actions.append(('recv', n))

    def recvuntil(self, b):
        self._actions.append(('recvuntil', b))

    def recvall(self):
        self._actions.append(('recvall', None))

    def send(self, b):
        self._actions.append(('send', b))

    def script(self, filename=None):
        """
        write the whole script
        """
        result = self._template.render(actions=self._actions,
                                       arguments=self._arguments,
                                       **self._kwargs)
        if filename:
            with open(filename, 'w') as f:
                f.write(result)
        return result
