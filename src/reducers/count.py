from typing import Dict, Any, Union

from .abstracts import Reducer


class CountReducer(Reducer):

    hash_table: Dict[str, int] = {}
    current_word: Union[str, None] = None
    current_count: int = 0

    def reduce(self, line: str) -> Any:
        word, count = line.split('\t', 1)

        try:
            word_count = int(count)
        except ValueError:
            return

        if self.current_word == word:
            self.current_count += word_count
        else:
            if self.current_word:
            # write result to STDOUT
                print('%s\t%s' % (self.current_word, self.current_count))
            self.current_count = word_count
            self.current_word = word

    def finish(self) -> Any:
        for key, value in self.hash_table.items():
            print(f"{key}\t{value}")
