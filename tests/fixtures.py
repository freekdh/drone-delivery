from pytest import fixture

from problem.problem import Problem


@fixture(scope="session")
def full_problem():
    data_file = "input/busy_day.in"
    return Problem.from_file(data_file)
