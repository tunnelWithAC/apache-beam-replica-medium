from itertools import groupby


class Transform:
    def __init__(self):
        self.children = []
        self.label = self.__class__.__name__

    def __rshift__(self, label):
        self.label = label
        return self

    def __or__(self, other):
        self.children.append(other)
        return other

    def __call__(self, input=None):
        assert input is not None, 'input must not be None'

        collected_values = []
        for output in map(self.expand, input):
            # use try/except as quick hack for checking if output is iterable
            try:
                # do this for transforms
                for o in output:
                    collected_values.append(o)
            except:
                collected_values.append(output)

        if len(self.children) > 0:
            for child in self.children:
                yield from child(collected_values)
        else:
            if isinstance(self, GroupBy):
                yield collected_values
            else:
                for value in collected_values:
                    yield value

    def expand(self, input_or_inputs):
        raise NotImplementedError

    def __str__(self):
        """Serialise the tree recursively as parent -> (children)."""
        childstring = ", ".join(map(str, self.children))
        return f"{self.label!s} -> ({childstring})"


class Create(Transform):
    def __init__(self, input_or_inputs):
        super().__init__()
        self.input_or_inputs = input_or_inputs

    def expand(self, input_or_inputs):
        yield input_or_inputs

    def __call__(self):
        yield from super().__call__(self.input_or_inputs)


class GroupBy(Transform):
    def __init__(self):
        super().__init__()

    def __call__(self, input):

        for key, group in groupby(input, self.get_key()):
            values = [item for item in group]
            transform_output = [{"key": key, "values": values}]

            if len(self.children) > 0:
                for child in self.children:
                    yield from child(transform_output)
            else:
                yield transform_output

    @staticmethod
    def get_key():
        return lambda x: x[0]
