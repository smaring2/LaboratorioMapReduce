from mrjob.job import MRJob
from mrjob.step import MRStep

class AverageSalaryByEmployee(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_salaries,
                   reducer=self.reducer_avg_salary)
        ]

    def mapper_get_salaries(self, _, line):
        parts = line.split(',')
        if parts[0] != 'idemp':
            idemp = parts[0]
            salary = float(parts[2])
            yield idemp, salary

    def reducer_avg_salary(self, idemp, salaries):
        total_salary = 0
        count = 0
        for salary in salaries:
            total_salary += salary
            count += 1
        yield idemp, total_salary / count

if __name__ == '__main__':
    AverageSalaryByEmployee.run()