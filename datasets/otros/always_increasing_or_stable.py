from mrjob.job import MRJob
from mrjob.step import MRStep

class AlwaysIncreasingOrStable(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        company, price, date = line.split(',')
        yield company, float(price)

    def reducer(self, company, values):
        prices = list(values)
        increasing_or_stable = all(x <= y for x, y in zip(prices, prices[1:]))

        if increasing_or_stable:
            yield company, "Increasing or Stable"

if __name__ == '__main__':
    AlwaysIncreasingOrStable.run()
