#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provide a behave shell to simplify creation of feature files
and running features, etc.

    context.command_result = behave_shell.behave(cmdline, cwd=context.workdir)
    behave_shell.create_scenario(scenario_text, cwd=context.workdir)
    behave_shell.create_step_definition(context.text, cwd=context.workdir)
    context.command_result = behave_shell.run_feature_with_formatter(
            context.features[0], formatter=formatter, cwd=context.workdir)

"""

from __future__ import absolute_import, print_function, with_statement
from behave4cmd0.__setup import HERE, TOP
import os.path
import six
import subprocess
import sys
import shlex
if six.PY2:
    import codecs


# HERE = os.path.dirname(__file__)
# TOP  = os.path.join(HERE, "..")

# -----------------------------------------------------------------------------
# CLASSES:
# -----------------------------------------------------------------------------
class CommandResult(object):
    """
    ValueObject to store the results of a subprocess command call.
    """
    def __init__(self, **kwargs):
        self.command = kwargs.pop("command", None)
        self.returncode = kwargs.pop("returncode", 0)
        self.stdout = kwargs.pop("stdout", "")
        self.stderr = kwargs.pop("stderr", "")
        self._output = None
        if kwargs:
            names = ", ".join(kwargs.keys())
            raise ValueError("Unexpected: %s" % names)

    @property
    def output(self):
        if self._output is None:
            output = self.stdout
            if self.stderr:
                output += "\n"
                output += self.stderr
            self._output = output
        return self._output

    @property
    def failed(self):
        return self.returncode != 0

    def clear(self):
        self.command = None
        self.returncode = 0
        self.stdout = ""
        self.stderr = ""
        self._output = None


class Command(object):
    """
    Helper class to run commands as subprocess,
    collect their output and subprocess returncode.
    """
    DEBUG = False
    COMMAND_MAP = {
        "behave": os.path.normpath("{0}/bin/behave".format(TOP)),
        "oneliner": os.path.normpath("{0}/oneliner".format(TOP)),
        "curl": "curl -#",
    }

    @classmethod
    def _transform_command(cls, cmdargs):
        real_command = cls.COMMAND_MAP.get(cmdargs[0], None)
        if real_command:
            cmdargs[:1] = shlex.split(real_command)

    @classmethod
    def run(cls, command, cwd=".", **kwargs):
        """
        Make a subprocess call, collect its output and returncode.
        Returns CommandResult instance as ValueObject.
        """
        assert isinstance(command, six.string_types)
        command_result = CommandResult()
        command_result.command = command

        cmdargs = shlex.split(command)
        Command._transform_command(cmdargs)

        # -- RUN COMMAND:
        try:
            process = subprocess.Popen(cmdargs,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True,
                                       cwd=cwd, **kwargs)
            out, err = process.communicate()
            process.poll()
            assert process.returncode is not None
            command_result.stdout = out
            command_result.stderr = err
            command_result.returncode = process.returncode
            if cls.DEBUG:
                print("shell.cwd={0}".format(kwargs.get("cwd", None)))
                print("shell.command: {0}".format(" ".join(cmdargs)))
                print("shell.command.output:\n{0};"
                      .format(command_result.output))
        except OSError as e:
            command_result.stderr = u"OSError: %s" % e
            command_result.returncode = e.errno
            assert e.errno != 0
        return command_result

    @classmethod
    def start(cls, command, cwd=".", **kwargs):
        """
        Run a subprocess in background.
        Returns Popen object.
        """
        assert isinstance(command, six.string_types)

        cmdargs = shlex.split(command)
        Command._transform_command(cmdargs)

        # -- RUN COMMAND:
        try:
            process = subprocess.Popen(cmdargs,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True,
                                       cwd=cwd, **kwargs)
        except OSError as e:
            print("OSError: %s" % e)
            out, err = process.communicate()
            print("OUT:\n", out)
            print("ERR:\n", err)
            assert e.errno != 0
        return process


# -----------------------------------------------------------------------------
# FUNCTIONS:
# -----------------------------------------------------------------------------
def run(command, cwd=".", **kwargs):
    return Command.run(command, cwd=cwd, **kwargs)


def start(command, cwd=".", **kwargs):
    return Command.start(command, cwd=cwd, **kwargs)


def behave(cmdline, cwd=".", **kwargs):
    """
    Run behave as subprocess command and return process/shell instance
    with results (collected output, returncode).
    """
    assert isinstance(cmdline, six.string_types)
    return run("behave " + cmdline, cwd=cwd, **kwargs)

# -----------------------------------------------------------------------------
# TEST MAIN:
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    command = " ".join(sys.argv[1:])
    output = Command.run(sys.argv[1:])
    print("command: {0}\n{1}\n".format(command, output))
