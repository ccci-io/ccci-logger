from datetime import datetime, timedelta

class TaskBot:

    def __init__(self, TASKS):
        self.TASKS = TASKS

        # FILL SEQUENCE
    def get_next(self):
        if self.ls == []:
            self.schedule(7)
        return self.ls.pop(0)

    def schedule(self, days_forward):
        self.now = datetime.now()
        
        self.start = self.now.replace(minute=0, hour=0)
        noon =  self.start + timedelta(days=1)   #12AM
        self.reset = noon
        
        self.ls = []
        tasks = self.TASKS.copy()

        #datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        #self.now.replace(minute=0, hour=0)
        for task in tasks:
            if type(task['action']) == str:
                self.create_task(task)
            elif type(task['action']) == list:
                print(task)
        self.ls.append(['datetime', 'git_pull'])

    def create_task(self, task):
        
        action = task.pop('action')
        
        bin_keys = [
            'minute',   # 1
            'hour',     # 2
            'day',      # 4
            'month',    # 8
            'year',     # 16
            'weekday',  # 32
        ]

        replace = {
            'millisecond': 0,
            'second': 0,
        }

        
       
        for i, k in enumerate(bin_keys):
            if k in task:
                o += 2**i

        on = ''

        for key in bin_keys[::-1]:
            n = 2**bin_keys.index(key)
            if o >= n:
                if key == 'weekday':
                    weekday = task.pop('weekday')
                
                if on != '':
                    on = key
                o -= n
                #getattr(dt, key)()
                #dt = datetime.now()
                # REPLACE POP
                #dt = dt.replace(**replace) + task[key]

        dt = datetime.now()

        if on == 'minute':
            
            for i in range(bin_keys.index(on), 4):
                replace[bin_keys[i]] = 0
            dt = dt.replace(**replace) + timedelta(task)
        
        if on == 'hour':

            for i in range(bin_keys.index(on), 4):
                replace[bin_keys[i]] = 0
            dt = dt.replace(**replace) + timedelta(task)

        date_keys = ['year', 'month', 'day']
        time = {}

        if on == 'day':
            # IS TODAY THIS DAY?
            # IS TODAY THIS WEEK?

            if dt < self.now:
                dt += timedelta(hours=1)

            while dt < self.reset:
                dt += timedelta(hours=1)
                task['action']

        if on == 'year':
            # IS IT ON THIS YEAR?
            # IF SO IS IT
            match = True
            #################################################
            #### LOOP THROUGH ALL BUT MOVE TIME ELEMENTS TO TIME
            for key in list(task.keys()):
                if key in date_keys:
                    if task[key] != getattr(dt, key)() or task[key] == 0:
                        match = False
                else:
                    if task[key] != 0:
                        time[key] = task.pop(key)
                        
            if match:
                task_dt = self.start + timedelta(**time)
                self.ls.append([task_dt, task])
  
            # task['year'] == getattr(dt, 'year')()
            # # # # # # # # # # # # # #
            ###########################





        if dt < self.now:
            dt += timedelta(hours=1)

        while dt < self.reset:
            dt += timedelta(hours=1)
            task['action']


        if o >= 32:
            
            if every != '':
                on = 'weekday'
            o -= 32

        if o >= 16:       # Do a task on this YEAR
            #do things
        
        elif o >= 8:        # Do a task every year on this MONTH.
            #do things
        
        elif o >= 4:        # Do a task every month on this DAY.

        elif o >= 2:        # Do a task every day on this HOUR.

            for i in range(self.forward*24):
                delta = self.now.replace(**task) + timedelta(hours=i) - self.now
                if delta > 0 and delta < timedelta(days=self.forward):
                    self.ls.append([delta, action])

        elif o = 1:         # Do a task every hour on this MINUTE.
            dt = datetime.now()
            dt = dt.replace(**replace) + task['minute']
            if dt < self.now:
                dt += timedelta(hours=1)

            while dt < self.reset:
                dt += timedelta(hours=1)
                task['action']
        


        replace['day'] = 0

        elif 4 <= o < 8:    # Do a task every month on this DAY.
            for i in range(self.forward):
                delta = self.now.replace(**task) + timedelta(days=i) - self.now
                if delta > 0 and delta < timedelta(days=self.forward):
                    self.ls.append([delta, action])

        replace['month'] = 0
        
        elif 8 <= o < 16:   # Do a task every year on this MONTH.
            # Do things
            
        elif 16 <= o < 32:  # Do a task on this YEAR
            # Do things

        if 32 <= o:
            weekday = task.pop('weekday')

        elif 36 <= o:
            # Additional operation to compare if day/month/year match the weekday. (in Jan 2020 Sundays 5pm send data)
            'hello'
                

    def check_state(self, task):
        arg = task['hour'][0] < self.now.hour() < task['hour'][1]



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
