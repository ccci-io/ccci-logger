

class TaskBot:
    def __init__(self, tasks):
        self.tasks = tasks
        self.ls = []

        # FILL SEQUENCE 
    def get_next(self):
        if len(self.ls) < 5:
            self.schedule()
        
        return self.ls.pop(0)

    def schedule(self):
        for task in self.tasks:
            if type(task['task']) == str:
                print(task)
            elif type(task['task']) == list:
                print(task)
            

TASKS = [
    {   # Run pull request from git at <daily:12>
        'task': 'git_pull', # Function
        'weekly': 0,        # On <1-7> Monday. <0> for all. (DEFAULT=0)
        'monthly': 0,       # On <1-31>th day of month. <0> for all. (DEFAULT=0)
        'daily': 12,        # On <1-24>th hour of day. <0> for hour. (DEFAULT=0)
        'hourly': 15,       # On <1-60>th minute of hour. (DEFAULT=0)
    },
    {   # Turn on the modem on <daily:11-13>th hour of every day.
        'task': ['modem_on', 'modem_off'],
        'daily': [11, 13],
    },
]