class Authorizer(object):

    class Judgement:

        def __init__(self, positive, restrictions=None):
            self._positive = positive
            self._restrictions = restrictions

        def is_granted(self):
            return self._positive is True

        def is_rejected(self):
            return not self.is_granted()

        def has_restrictions(self):
            return self._restriction is not None

        def get_restriction(self):
            return self._restriction

    def __init__(self, policy):
        self._policy = policy

    def __call__(self, identity):
        raise NotImplemented


class NoAuthorizer(Authorizer):

    def __init__(self):
        super(NoAuthorizer, self).__init__(None)

    def __call__(self, identity):
        return Authorizer.Judgement(True)


