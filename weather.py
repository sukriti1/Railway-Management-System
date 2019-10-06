import Tkinter as tk
import sys
egg_path='C:\Python27\pyowm-2.4.0-py2.7.egg'    #to obtain module pyowm
sys.path.append(egg_path)
import pyowm
import time
import json
from datetime import datetime
from collections import OrderedDict

class WeatherInfo(tk.Tk):
    templates = OrderedDict([
        ('temp', 'Temperature: {temp:.1f} C'),
        ('humid', 'Humidity: {humid}%'),
        ('status', 'Status: {status}'),
        ('sunrise', 'Sunrise at {sunrise:%H:%M:%S}'),
        ('sunset', 'Sunset at {sunset:%H:%M:%S}'),
        ('day_length', 'Day length: {day_length:.1f} h'),
        ('night_length', 'Night length: {night_length:.1f} h')])

    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_title('Weather')
        self.tk_info = {key: tk.StringVar(
            self, value='') for key in WeatherInfo.templates}

        self.ask = tk.LabelFrame(self, text='Location') #location label
        self.ask.pack(fill='both', expand='yes')
        self.kw_label = tk.Label(self.ask, text='City:') #city label
        self.kw_label.pack(side=tk.LEFT)
        self.kw = tk.Entry(self.ask)   #city entry
        self.kw.pack(side=tk.LEFT)
        self.rb = tk.Button(self.ask, text='Go', command=self.main) #go button
        self.rb.pack(side=tk.RIGHT)
        self.owm = pyowm.OWM('8532178252fc66e6baa1298613be5eeb')

        self.output = tk.LabelFrame(self, text='Information')
        self.output.pack(fill='both', expand='yes')
        self.labels = []
        for key in WeatherInfo.templates:
            self.labels.append(
                tk.Label(self.output, textvariable=self.tk_info[key]).pack())
        button = tk.Button(master=self, text='Quit', command=self._quit)
        button.pack(side=tk.BOTTOM)

    def search(self):
        obs = self.owm.weather_at_place(self.kw.get())
        try:
            return json.loads(obs.get_weather().to_JSON())
        except AttributeError:
            self.tk_info['temp'].set('Pick a city to display weather.')

    def parse(self, w):
        parsed_weather = {'temp': w['temperature']['temp'] - 273.15,
                          'humid': w['humidity'],
                          'status': w['status'],
                          'sunrise': datetime.fromtimestamp(w['sunrise_time']),
                          'sunset': datetime.fromtimestamp(w['sunset_time']),
                          'day_length': (w['sunset_time'] - w['sunrise_time']) / 3600,
                          'night_length': 24 - (w['sunset_time'] - w['sunrise_time']) / 3600}
        return parsed_weather

    def update(self, report):
        for key, template in WeatherInfo.templates.items():
            self.tk_info[key].set(template.format(**report))

    def main(self):
        report = self.search()
        if report:
            self.update(self.parse(report))

    def _quit(self):
        self.quit()
        self.destroy()

    
