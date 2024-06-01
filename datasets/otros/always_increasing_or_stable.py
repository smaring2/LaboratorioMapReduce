from mrjob.job import MRJob
from mrjob.step import MRStep

class BlackDay(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_black_day)
        ]

    def mapper(self, _, line):
        fields = line.split(',')
        if len(fields) == 3:
            company, price, date = fields
            yield date, float(price)

    def reducer(self, date, prices):
        yield None, (date, sum(prices))

    def reducer_find_black_day(self, _, date_sums):
        black_day = min(date_sums, key=lambda x: x[1])
        yield 'Black Day', black_day

if __name__ == '__main__':
    BlackDay.run()
