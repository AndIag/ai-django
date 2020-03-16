from rest_framework.response import Response as RFResponse


class Action(object):
    """Configuration to change CustomerService.consumed"""

    CONSUMES = 'consumes'
    FREES = 'frees'

    @staticmethod
    def _is_valid_action(action):
        return action == Action.CONSUMES or action == Action.FREES

    def __init__(self, action=None, service=None, customer=None, amount=None):
        super(Action, self).__init__()

        if not self._is_valid_action(action):
            raise ValueError('Action must mach {}'.format([self.CONSUMES, self.FREES]))

        self.action = action
        self.service = service
        self.customer = customer
        self.amount = amount


class Response(RFResponse):
    """
    Extends django-rest-framework behavior adding an Action used for TSquadMiddleware to update
    CustomerService.consumed.
    """

    # noinspection PyShadowingNames
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        actions=None
    ):
        self.actions = actions
        super(Response, self).__init__(data, status, template_name, headers, exception, content_type)
