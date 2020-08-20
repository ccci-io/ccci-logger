from datetime import datetime, timedelta

class TaskBot:

    KEYS = [
        'second',       # 1     # 0
        'minute',       # 2     # 1
        'hour',         # 4     # 2
        'day',          # 8     # 3
        'month',        # 16    # 4
        'year',         # 32    # 5
        'isoweekday',   # 64    # 6
    ]
    
    ls =  []
    exe = []

    def __init__(self, TASKS):
        self.TASKS = TASKS

        # FILL SEQUENCE
    def get_next(self):
        dt_now = datetime.now()
        if self.ls == []:
            self.schedule()
        print(dt_now-self.ls[0])

        return dt_now-self.ls.pop(0)

    def byDateTime(self, elem):
        return elem[0]

    def sort_ls(self):
        self.ls.sort(key=self.byDateTime)

    def time_to_minute(self, minute):
        dt_now = datetime.now()
        dt = now.replace(minute=minute)

        if dt < dt_now:
            dt += timedelta(hours=1)
        
        return dt


    def branch_task(self, task):
        task_on = {}
        task_off = {}
        for key in task.keys():
            task_on[key] = task[key][0]
            task_off[key] = task[key][1]
        
        return task_on, task_off

    """def check_state(self, task, task_on, task_off):
        match = True
        if task_on == 'isoweekday':
            self.now.isoweekday()
        for key in KEYS:
            try:
                if not task[key][0] < getattr(self.now, key)() <= task[key][1]:
                    match = False
                    break
                if key == task_on:
                    break
            except:
                continue
        
        return match"""


    def check_state(self, arg_task):
        task = arg_task.copy()
        action = task.pop('action')[0]
        if 'isoweekday' in task:
            isoweekday_on, isoweekday_off = task.pop('isoweekday')

        dt_now = datetime.now()
        task_on, task_off = self.branch_task(task)
        dt_on, dt_off = dt_now.replace(**task_on), dt_now.replace(**task_off)
        if dt_on <= dt_now < dt_off:
            self.exe.append(action)
        


    def schedule(self):
        self.now = datetime.now()
        self.start = self.now.replace(second=0, minute=0, hour=0)
        midnight =  self.start + timedelta(days=1)   #12AM
        self.reset = midnight
        self.ls = []
        self.exe = []
        tasks = self.TASKS.copy()

        for task in tasks:
            
            if type(task['action']) == str:
                self.create_task(task)
            elif type(task['action']) == list:
                self.check_state(task)
                task_on, task_off = self.branch_task(task)
                self.create_task(task_on)
                self.create_task(task_off)
                # self.create_task(self.branch_task(task))
        
        self.sort_ls()
                    


    def iterate_dt(self, task, action, on, add):
        dt_now = datetime.now()
        replace = {}

        for i in range(0, self.KEYS.index(on)+1):
            replace[self.KEYS[i]] = 0

        dt = dt_now.replace(**replace) + timedelta(**task)
        
        if dt < self.now:
            dt += add

        while dt < self.reset:
            self.ls.append([dt, action])
            dt += add


    def match_date(self, task):
        date_keys = ['isoweekday', 'year', 'month', 'day']
        time = {}
        dt_now = datetime.now()
        match = True

        #### LOOP THROUGH ALL BUT MOVE TIME ELEMENTS TO DICT(time)
        for key in list(task.keys()):
            if key in date_keys:
                if task[key] != getattr(dt_now, key) and task[key] != 0:
                    match = False
            else:
                if task[key] != 0:
                    time[key] = task.pop(key)
        return match, time

    def append_time(self, time, action):
        dt = self.start.replace(**time)
        if dt > self.now:
            self.ls.append([dt, action])


    def create_task(self, task):
        action = task.pop('action')
        on = ''
        o = 0

        ### ENGINE START ###

        for i, k in enumerate(self.KEYS):
            if k in task:
                o += 2**i

        for key in self.KEYS[::-1]:
            n = 2**self.KEYS.index(key)
            if o >= n:
                if on != '':
                    on = key
                o -= n

        ### ENGINE END ###
        
        if on == 'second':
            add = timedelta(minutes=1)
            self.iterate_dt(task, action, on, add)

        elif on == 'minute':
            add = timedelta(hours=1)
            self.iterate_dt(task, action, on, add)
            
        else:
            match, time = self.match_date(task)
            if match:
                self.append_time(time, action)
            
        return on

    
