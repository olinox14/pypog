'''
Tipog tests

Usage:
  tipog [-v] <filename> [-o <output>]

Options:
  -v --verbose       Verbose print
  -o --output        Register the results in <output> file (.json)
  -h --help          Show this screen.
  --version          Show version.
'''

import cProfile
from importlib import import_module
import json
import os
import timeit

from docopt import docopt
import yaml

__version__ = "0.2"

class ItpogDataError(IOError):
    pass

class ItPog(object):
    def __init__(self, ipfile, verbose=False, output=None, outfilename=None):
        try:
            with open(ipfile, "r") as f:
                data = yaml.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("no file named '{}'".format(ipfile))
        except yaml.scanner.ScannerError:
            raise ItpogDataError("unreadable yaml file '{}'".format(ipfile))

        if not data:
            raise ItpogDataError("file '{}' is empty".format(ipfile))

        self.ipfile = ipfile
        self.ipdata = data

        self.verbose = verbose
        self.output = output
        self.outfilename = outfilename
        self.out_result = []

    @classmethod
    def run_file(cls, *args, **kwargs):
        """ convenient method to load a file and run the tests
        returns an ItPog object"""
        try:
            itpog = cls(*args, **kwargs)
            itpog.run()
        except Exception as e:
            print("{}: {}".format(e.__class__.__name__, str(e)))
        return itpog

    def run(self):
        """ run the jobs as programmed in the given file """
        for name, imp in self.ipdata["imports"].items():
            try:
                globals()[name] = import_module(imp)
            except (ModuleNotFoundError, ImportError):
                raise ItpogDataError("unable to import '{}'".format(imp))
        try:
            jobs = self.ipdata["jobs"]
        except KeyError:
            raise ItpogDataError("missing 'jobs' entry")

        for function_name, job in jobs.items():
            try:
                self._run_job(function_name, job)
            except Exception as e:
                print("{}: {}".format(e.__class__.__name__, str(e)))

        if self.output:
            if not self.outfilename:
                self.outfilename = "{}_result.json".format(os.path.splitext(self.ipfile)[0])

            outfilepath = os.path.join(".", self.outfilename)
            try:
                os.remove(outfilepath)
            except FileNotFoundError:
                pass
            with open(outfilepath, "w+") as f:
                json.dump(self.out_result, f)

        print("** End of the tests")

    def _run_job(self, function_name, job):
            try:
                function = eval(function_name)
            except NameError:
                raise NameError("unknown function ('{}')".format(function_name))

            if self.verbose:
                print("** Test function '{}'".format(function_name))

            try:
                args_lst = job["args"]
            except KeyError:
                args_lst = [[]]

            try:
                validator_str = job["validator"]
                try:
                    validator = eval(validator_str)
                    if self.verbose:
                        print("> validator: '{}'".format(validator_str))
                except NameError:
                    raise ItpogDataError("unknown function as validator ('{}')".format(validator_str))

            except (TypeError, KeyError, SyntaxError):
                validator = None

            for args in args_lst:
                call_str = "{}(*{})".format(function_name, args)

                print(">> {}".format(call_str))

                exectime = self.ittime(call_str)
                print("\t> Run in {} ms.".format(exectime))

                if self.verbose:
                    self.profile(call_str)

                if validator:
                    valid = self.validate(function, validator, args)
                    print("\t> Validated: {}".format(valid))

                if self.output:
                    last_result = {"call": call_str, "result": function(*args), "exectime": exectime}
                    try:
                        last_result.update(job["infos"])
                    except KeyError:
                        pass
                    self.out_result.append(last_result)

            if self.verbose:
                print("------------------------------")


    @staticmethod
    def profile(_call):
        """ Use the cProfile module to measure the execution time of each call
            _call has to be a string
        """
        cProfile.run(_call, sort='nfl')

    @staticmethod
    def ittime(_call):
        """ returns the execution time in milli-seconds
            _call has to be a string
            (ex: 'time.sleep(1)', which will return 1000)
        """
        number, t = 1, 0
        while t < 10 ** 8:
            t = timeit.timeit(lambda: eval(_call), number=number)
            if t >= 0.1:
                return 1000 * t / number
            number *= 10
        else:
            return -1

    @staticmethod
    def validate(fct, validator, args=[], kwargs={}):
        """ compare the results of 'fct' and 'validator' methods,
        with the same 'args' and 'kwargs' arguments """
        result = fct(*args, **kwargs)
        attended = validator(*args, **kwargs)
        return result == attended

    @staticmethod
    def generate_sample(filename="itpog_sample_file.yml"):
        """ generate a sample yaml configuration file """
        data = {"imports": {"time": "time", "math": "math"},
                "jobs": {
                          "time.sleep": {"infos": {"note": "x second attended"},
                                    "args": [[0.1], [1]],
                                    "validator": ""},
                          "math.pow":  {"infos": {},
                                    "args": [[1, 2], [3, 2], [3, 3], [4, 2]],
                                    "validator": "lambda x, y: x**y"}
                         }
                }
        with open(os.path.join(".", filename), "w+") as f:
            yaml.dump(data, f)


if __name__ == "__main__":

    sysargs = docopt(__doc__, version=__version__)

    itpog = ItPog.run_file(sysargs["<filename>"], sysargs["--verbose"], sysargs["--output"], sysargs["<output>"])



