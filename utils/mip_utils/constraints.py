from utils.mip_utils.linear_expression import LinearExpression


class EqualityConstraint:
    def __init__(self, lhs, rhs):
        assert isinstance(lhs, LinearExpression)
        assert isinstance(rhs, (float, int))
        self.rhs = rhs
        self.lhs = lhs


class LE_InequalityConstraint:
    """
    Less than or equal to inequality constraint
    """

    def __init__(self, lhs, rhs):
        assert isinstance(lhs, LinearExpression)
        assert isinstance(rhs, (float, int))
        self.rhs = rhs
        self.lhs = lhs
