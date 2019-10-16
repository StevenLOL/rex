import textwrap
from .scripter import Scripter
from ..exploit import Exploit
from ..common.enums import CrashInputType

class PYScripter(Scripter):
    """
    A scripter to generate python exploit automatically
    """

    @property
    def prologue(self):
        return textwrap.dedent("""
                               import sys
                               import time
                               import nclib
                            
                               if len(sys.argv) < 3:
                                   print("%s: <host> <port>" % sys.argv[0])
                                   sys.exit(1)
                            
                               r = nclib.Netcat((sys.argv[1], int(sys.argv[2])), udp=False)
                               """)

    @property
    def epilogue(self):
        return "\nr.interactive()\n"

    def recv(self):
        """
        handles a single recv command
        """
        raise NotImplementedError("Does not have the ability to recv yet")

    def send(self, raw_data):
        """
        handles a single send command
        """
        script = "\npayload = %s\n" % raw_data
        script += "r.send(payload)\n"
        return script

    def script(self, exploit):
        """
        script body
        """

        assert isinstance(exploit, Exploit), "Scripter only can work on an Exploit object"
        # only tcp program right now
        if exploit.crash.input_type not in (CrashInputType.TCP, CrashInputType.STDIN):
            raise NotImplementedError("Unsupported crash input type %s." % exploit.crash.input_type)

        return self.send(exploit.dump())
