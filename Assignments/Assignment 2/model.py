from assign2_support import *

class PVData(object):
    """Class to hold the PV data for a given date."""
    def __init__(self):
        """Constructs an instance of data."""
        self._dateStr = yesterday()
        self._arraydict = {}
        self._data = load_data(self._dateStr)
                          

    def change_date(self, date): #re-initialize 
        if date != self._dateStr:
            self._dateStr = date
            self._data = load_data(self._dateStr)
            
            arraydict = {}
            for i, array in enumerate(ARRAYS):
                powers = []
                for row in self._data:
                    powers.append(row[3][i])
                arraydict[array] = powers   
            self._arraydict = arraydict
            
            self._temperature = []
            self._sunlight = []
            for i in self._data:
                self._temperature.append(i[1])
                self._sunlight.append(i[2])
            
    def get_date(self):
        return self._dateStr

    def get_time(self, time_index):
        timelist = []
        for i in self._data:
            timelist.append(i[0])
        return timelist[time_index]

    def get_temperature(self):
        self._temperature = []
        for i in self._data:
            self._temperature.append(i[1])
        return self._temperature     

    def get_sunlight(self):
        self._sunlight = []
        for i in self._data:
            self._sunlight.append(i[2])
        return self._sunlight

    def get_power(self, array):
        return self._arraydict.get(array, 0)
