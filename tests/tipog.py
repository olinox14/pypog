'''
Tipog tests

Usage:
  tipog [-v] <filename> [-o <output>]

Options:
  -v --verbose       Verbose result
  -o --output        Register the results in <output> file (json)
  -h --help          Show this screen.
  --version          Show version.
'''

import cProfile
import json
import os
import sys
import timeit

from docopt import docopt
import yaml


__version__ = "0.1"

sysargs = docopt(__doc__, version=__version__)

yaml_file = sysargs["<filename>"]

try:
    with open(yaml_file, "r") as f:
        data = yaml.load(f)
except FileNotFoundError:
    print("ERR: no file named '{}'".format(yaml_file))
    sys.exit(1)
except yaml.scanner.ScannerError:
    print("ERR: unreadable yaml file '{}'".format(yaml_file))
    sys.exit(1)

if not data:
    print("ERR: empty yaml file '{}'".format(yaml_file))
    sys.exit(1)

for to_import in data["imports"]:
    try:
        # TODO: avoid the 'exec'
        exec(to_import)
    except (ModuleNotFoundError, ImportError):
        print("ERR: unable to import '{}'".format(to_import))
        sys.exit(1)

try:
    jobs = data["jobs"]
except KeyError:
    print("ERR: missing 'jobs' entry")
    sys.exit(1)




def profile(_call, verbose=False):

    print(">> {}".format(_call))

    if verbose:
        cProfile.run(_call, sort='nfl')

    number = 1
    t = 0
    while 1:
        t = timeit.timeit(lambda: eval(_call), number=number)
        if t >= 0.1:
            break
        elif number > 10000000:
            print("ERR: unable to compute the execution time")
            number = "err"
            t = "?"
            break
        number *= 10

    return t / 1000



def validate(fct, validator, args, verbose=False):
    result = fct(*args)
    attended = validator(*args)
    return result == attended

to_register = []

for function_name, job in jobs.items():

    try:
        function = eval(function_name)
    except NameError:
        print("ERR: unknown function ('{}')".format(function_name))
        continue

    if sysargs["--verbose"]:
        print("** Test function '{}'".format(function_name))

    try:
        args_lst = job["args"]
    except KeyError:
        args_lst = [[]]

    try:
        validator_str = job["validator"]
        try:
            validator = eval(validator_str)
            if sysargs["--verbose"]:
                print("> validator: '{}'".format(validator_str))
        except NameError:
            print("ERR: unknown function as validator ('{}')".format(validator_str))
    except (TypeError, KeyError):
        validator = None

    for args in args_lst:
        call_str = "{}(*{})".format(function_name, args)

        exectime = profile(call_str, sysargs["--verbose"])
        print("\t> Run in {} ms.".format(exectime))

        if validator:
            valid = validate(function, validator, args, sysargs["--verbose"])
            print("\t> Validated: {}".format(valid))

        if sysargs["--output"]:
            last_result = {"call": call_str, "result": function(*args), "exectime": exectime}
            try:
                last_result.update(job["infos"])
            except KeyError:
                pass
            to_register.append(last_result)

    if sysargs["--verbose"]:
        print("------------------------------")

if sysargs["--output"]:
    output_name = sysargs["<output>"]
    if not output_name:
        output_name = "{}_result".format(os.path.splitext(sysargs["<filename>"])[0])

    reg_file_path = os.path.join(".", output_name)
    try:
        os.remove(reg_file_path)
    except FileNotFoundError:
        pass
    with open(reg_file_path, "w+") as f:
        json.dump(to_register, f)

print("** End of the tests")
