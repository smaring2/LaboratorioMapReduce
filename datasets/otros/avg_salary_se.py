from mrjob.job import MRJob
from mrjob.step import MRStep

class AverageSalaryBySector(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_salaries,
                   reducer=self.reducer_avg_salary)
        ]

    def mapper_get_salaries(self, _, line):
        parts = line.split(',')
        if parts[0] != 'idemp':
            sececon = parts[1]
            salary = float(parts[2])
            yield sececon, salary

    def reducer_avg_salary(self, sececon, salaries):
        total_salary = 0
        count = 0
        for salary in salaries:
            total_salary += salary
            count += 1
        yield sececon, total_salary / count

if __name__ == '__main__':
    AverageSalaryBySector.run()
