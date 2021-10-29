class activationtask:
    def __init__(self,core,idle):
        self.core_=core
        self.idle_=idle
        self.dp=0
        self.output=[0,0,0]

    def start_task(self):
        work=automatedact
        work.execute()
        self.running=True

    def stop_task(self):
        self.running=False

    def isrunning(self):
        return  self.running

    def set_idle(self,idle):
        self.idle_=idle

    def getN(self,coeff,cutoff,dt,autocutoff):
        if self.core_.is_sequence_running() and self.core_.get_bytes_per_pixel==2:
            abort=False
            counter1=0
            counter2=0
            width=self.core_.get_image_width()
            height = self.core_.get_image_height()
