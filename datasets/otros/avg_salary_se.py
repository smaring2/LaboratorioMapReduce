from mrjob.job import MRJob
from mrjob.step import MRStep

class AvgSalaryBySector(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_salaries,
                   reducer=self.reducer_calculate_avg)
        ]

    def mapper_get_salaries(self, _, line):
        fields = line.split(',')
        if len(fields) == 4:
            sececon = fields[1]
            salary = float(fields[2])
            yield sececon, salary

    def reducer_calculate_avg(self, key, values):
        total_salary = 0
        count = 0
        for salary in values:
            total_salary += salary
            count += 1
        yield key, total_salary / count

if __name__ == '__main__':
    AvgSalaryBySector.run()
