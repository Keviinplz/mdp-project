from typing import List

from .abstracts import Mapper
from src.lib.utils import str2timestamp
from datetime import datetime

class UserMapper(Mapper):
    in_sep : str = ","
    out_sep : str = "\t"
    ts_sep : str = "#"
    firstTime : str = "2022-04-01 12:44:10.315"
    DATETIME_FORMAT_STRING: List[str] = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]
    
    def __init__(self):
        # set the first timestamp from the string as seconds
        self.first_ts = str2timestamp(self.firstTime, format = self.DATETIME_FORMAT_STRING)
        # now to miliseconds
        self.first_ts *= 1000
    
    def map(self, line: str) -> None:
        try:
            (time, user_id, _, _, _, mod) = line.split(self.in_sep)
        except:
            # if there is error skip the line
            return
        
        # if mod 1, discard line
        if mod == "0":
            # add time to the starting time (all in miliseconds)
            ms : int = int(time) + self.first_ts
            # now convert it to datetime (may lose some precision in division :c)
            timestamp : datetime = datetime.utcfromtimestamp(ms//1000).replace(microsecond=ms%1000*1000)
            out_timestamp : str = str(timestamp)
            if len(out_timestamp) < 26:
                out_timestamp += "."
                out_timestamp = out_timestamp.ljust(26, '0')
            
            # change line structure
            # user  timestamp  count(1)
            outLine : str = user_id + self.out_sep + out_timestamp + self.out_sep + "1"
            # output line
            print(outLine)
