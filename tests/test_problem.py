from problem.loaders import Problem


def test_problem_class():
    data_file = "input/busy_day.in"
    Problem.from_file(data_file)
