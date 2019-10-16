"""
Module to make script generation customizable
"""
from abc import abstractproperty, abstractmethod

class Scripter:
    """
    A scripter object is the abstraction of exploit generation.
    It is used to generate standalone exploits according to user provided specifications
    """
    def __init__(self):
        pass

    @abstractproperty
    def prologue(self):
        raise NotImplementedError("prologue is an abstract method!")

    @abstractproperty
    def epilogue(self):
        raise NotImplementedError("epilogue is an abstract method!")

    @abstractmethod
    def script(self, exploit):
        raise NotImplementedError("script is an abstract method!")

    def write_script(self, exploit, filename=None):
        """
        write the whole script
        """
        script = ""
        script = self.prologue
        script += self.script(exploit)
        script += self.epilogue
        if filename:
            with open(filename, 'w') as f:
                f.write(script)
        return script
