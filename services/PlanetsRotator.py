class PlanetsrotatorService:
    def __init__(self):
        self.all = []
        self.cursor = 0

    def add(self, planets):
        self.all.extend(planets)

    def next(self):
        if self.cursor == len(self.all):
            self.cursor = 0

        planet = self.all[self.cursor]
        self.cursor += 1

        return planet

    def count(self):
        return len(self.all)