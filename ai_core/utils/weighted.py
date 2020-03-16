class WeightedItem(object):
    """
    Works as a container to give items a weight in a given list.

    Overrides comparision methods to use 'weight' value
    """

    def __init__(self, key, weight: int = 0):
        self.key = key
        self.weight = weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __ge__(self, other):
        return self.weight >= other.weight

    def __gt__(self, other):
        return self.weight > other.weight


class WeightedList(object):
    """Wraps a list of 'WeightedItem' items to make it work as a dictionary"""
    items = []

    def __init__(self, *args: WeightedItem):
        self.items = list(args)

    def __getitem__(self, item):
        return next((x for x in self.items if x.key == item), None)
