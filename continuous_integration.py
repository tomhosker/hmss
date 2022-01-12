"""
This code defines a script which runs this repo's continuous integration
routines.
"""

# Standard imports.
import os
import pytest
import subprocess

# Local constants.
DEFAULT_MIN_CODE_COVERAGE = 50
DEFAULT_MIN_LINT_SCORE = 8

#############
# FUNCTIONS #
#############

def run_unit_tests(min_code_coverage=DEFAULT_MIN_CODE_COVERAGE):
    """ Run PyTest. """
    arguments = [
        "--cov-report", "term",
        "--cov-fail-under="+str(min_code_coverage),
        "--cov=."
    ]
    return_code = pytest.main(arguments)
    assert return_code == 0, "PyTest returned code: "+str(return_code)

def is_python_file(filename):
    """ Determine whether a given filename represents a Python file. """
    if filename and filename.endswith(".py"):
        return True
    return False

def run_linter_strictly(min_lint_score=DEFAULT_MIN_LINT_SCORE):
    """ Run PyLint, checking that EACH file reaches a given score. """
    arguments = ["pylint", "--fail-under="+str(min_lint_score)]
    for filename in os.listdir():
        if is_python_file(filename):
            subprocess.run(arguments+[filename], check=True)

def run_linter_indulgently(min_lint_score=DEFAULT_MIN_LINT_SCORE):
    """ Run PyLint, checking that all the files, taken as a WHOLE, reach a
    given score. """
    arguments = ["pylint", "--fail-under="+str(min_lint_score)]
    for filename in os.listdir():
        if is_python_file(filename):
            arguments.append(filename)
    subprocess.run(arguments+[filename], check=True)

def run_linter(min_lint_score=DEFAULT_MIN_LINT_SCORE, strict=False):
    """ Run PyLint """
    if strict:
        run_linter_strictly(min_lint_score=min_lint_score)
    else:
        run_linter_indulgently(min_lint_score=min_lint_score)

def run_continuous_integration():
    """ Run the continuous integration routines. """
    run_unit_tests()
    run_linter()

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    run_continuous_integration()

if __name__ == "__main__":
    run()
