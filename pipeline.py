class Pipeline:
    def __init__(self):
        self.start = None

    def __or__(self, start):
        self.start = start
        return start

    def run(self):
        results = []
        for element in self.start():
            results.append(element)
        return results

    @property
    def graph(self):
        return str(self.start)