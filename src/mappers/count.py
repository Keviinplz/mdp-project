from .abstracts import Mapper

class CountMapper(Mapper):
    
    def map(self, line: str) -> None:
        words = line.split()
        for word in words:
            print('%s\t%s' % (word, 1))