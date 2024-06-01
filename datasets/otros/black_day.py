from mrjob.job import MRJob
from mrjob.step import MRStep

class BlackDay(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        company, price, date = line.split(',')
        yield date, float(price)

    def reducer(self, date, values):
        yield None, (date, sum(values))

    def reducer_find_black_day(self, _, date_sums):
        black_day = min(date_sums, key=lambda x: x[1])
        yield black_day

if __name__ == '__main__':
    BlackDay.run()
