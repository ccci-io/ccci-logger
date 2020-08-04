from datetime import datetime, timedelta

class TaskBot:

    forward = 7 # DAYS TO LOOK AHEAD

    def __init__(self, TASKS):
        self.TASKS = TASKS

        # FILL SEQUENCE
    def get_next(self):
        if self.ls == []:
            self.schedule(7)
        return self.ls.pop(0)

    def schedule(self, days_forward):
        self.dt = datetime.now()
        self.now = {
            'second': dt.second(),
            'minute': dt.minute(),
            'hour': dt.hour(),
            'day': dt.day(),
            'month': dt.month(),
            'year': dt.year(),
            'weekday': dt.isoweekday(),
        }
        self.ls = []
        tasks = self.TASKS.copy()

        # Check if less then 1 week

        #datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        for task in tasks:
            if type(task['action']) == str:
                self.create_task(task)
            elif type(task['action']) == list:
                print(task)
        self.ls.append(['datetime', 'git_pull'])

    def create_task(self, task):
        
        action = task.pop('action')
        
        o = 0
        for i, k in enumerate(list(self.now.keys())):
            if k in task:
                o += 2**i

        if o < 2:
            for i in range(self.forward*24):
                delta = self.dt.replace(**task) + timedelta(hours=i) - self.dt
                if delta > 0 and delta < timedelta(days=self.forward):
                    self.ls.append([delta, action])
        
        if o < 4:
            for i in range(self.forward):
                delta = self.dt.replace(**task) + timedelta(days=i) - self.dt
                if delta > 0 and delta < timedelta(days=self.forward):
                    self.ls.append([delta, action])
                    

        if o >= 32:
            weekday = task.pop('weekday')

        if o >= 36:
            # Additional operation to compare if day/month/year match the weekday. (in Jan 2020 Sundays 5pm send data)
            'hello'
                

    def check_state(self, task):
        arg = task=['hour'][0] < self.now['hour'] < task['hour'][1]



TASKS = [
    {   # Run pull request from git at <daily:12>
        'action': 'git_pull',   # Function
        'minute': 5,            # On <1-60>th minute of hour. (DEFAULT=0)
        'hour': 12,             # On <1-24>th hour of day. <0> for every hour. (DEFAULT=0)
        #'day': 0,               # On <1-31>th day of month. <0> for every day. (DEFAULT=0)
        #'month': 0,             # On <1-12>th month of the year. <0> for every month. (DEFAULT=0)
        #'year': 0,              # On <2020+>th year. <0> for every year. (DEFAULT=0)
        #'weekday': 0,           # On <1-7> Monday. <0> for for every weekday. (DEFAULT=0)
    },
    {   # Turn on the modem on <daily:11-13>th hour of every day.
        'action': ['modem_on', 'modem_off'],
        'hour': [11, 13],
    },
]
