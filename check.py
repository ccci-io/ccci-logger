import datetime from datetime, timedelta

class TaskBot:
    def __init__(self, tasks):
        self.tasks = tasks
        self.ls = []

        # FILL SEQUENCE
    def get_next(self):
        if self.ls == []:
            self.schedule(30)
        return self.ls.pop(0)

    def schedule(self, max_ls):
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

        tasks = self.tasks.copy()

        # Check if less then 1 week

        #datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        for task in tasks:
            if type(task['task']) == str:
                self.create_task(task)
            elif type(task['task']) == list:
                print(task)
        self.ls.append(['datetime', 'git_pull'])

    def create_task(self, task):
        
        o = 0
        for i, k in enumerate(list(self.now.keys())):
            if k in task:
                o += 2**i
        
        if o < 64:
            # MODIFIED DICTIONARY TO EXCLUDE WEEKDAY AND TASK
            self.dt.replace() - self.dt

        if o >= 72:
            # Additional operation to compare if day/month/year match the weekday. (in Jan 2020 Sundays 5pm send data)
                

    def check_state(self, task):
        arg = task=['hour'][0] < self.now['hour'] < task['hour'][1]



TASKS = [
    {   # Run pull request from git at <daily:12>
        'task': 'git_pull', # Function
        #'second': 0,        # On <1-60>th second of minute. (DEFAULT=0)
        'minute': 5,        # On <1-60>th minute of hour. (DEFAULT=0)
        'hour': 12,         # On <1-24>th hour of day. <0> for every hour. (DEFAULT=0)
        #'day': 0,           # On <1-31>th day of month. <0> for every day. (DEFAULT=0)
        #'month': 0,         # On <1-12>th month of the year. <0> for every month. (DEFAULT=0)
        #'year': 0,          # On <2020+>th year. <0> for every year. (DEFAULT=0)
        #'weekday': 0,       # On <1-7> Monday. <0> for for every weekday. (DEFAULT=0)
    },
    {   # Turn on the modem on <daily:11-13>th hour of every day.
        'task': ['modem_on', 'modem_off'],
        'hour': [11, 13]
    },
]
