from mrjob.job import MRJob
from mrjob.step import MRStep

class SECountByEmployee(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_sectors,
                   reducer=self.reducer_count_sectors)
        ]

    def mapper_get_sectors(self, _, line):
        parts = line.split(',')
        if parts[0] != 'idemp':
            idemp = parts[0]
            sececon = parts[1]
            yield idemp, sececon

    def reducer_count_sectors(self, idemp, sececons):
        unique_sectors = set(sececons)
        yield idemp, len(unique_sectors)

if __name__ == '__main__':
    SECountByEmployee.run()
