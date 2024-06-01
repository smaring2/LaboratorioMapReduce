from mrjob.job import MRJob
from mrjob.step import MRStep

class MinMaxPriceByCompany(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        company, price, date = line.split(',')
        yield company, (float(price), date)

    def reducer(self, company, values):
        min_price = float('inf')
        max_price = float('-inf')
        min_date = None
        max_date = None

        for price, date in values:
            if price < min_price:
                min_price = price
                min_date = date
            if price > max_price:
                max_price = price
                max_date = date

        yield company, (min_date, min_price, max_date, max_price)

if __name__ == '__main__':
    MinMaxPriceByCompany.run()
