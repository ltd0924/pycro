class Peak:
    def __init__(self,x,y,value):
        self.x_=x
        self.y_=y
        self.value_=value

    def set(self,x,y,value):
        self.x_ = x
        self.y_ = y
        self.value_ = value

    def getX(self):
        return  self.x_

    def getY(self):
        return  self.y_

    def getvalue(self):
        return  self.value_

    def toString(self):
        return "["+self.x_+","+self.y_+","+self.value_+"]"

