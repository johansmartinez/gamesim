class RandomNumber():

    def __init__(self):
        self.a=9
        self.c=3
        self.m=256
        self.xi=4

    def calculate_ri(self):
        self.xi= ((self.a*self.xi)+self.c)%self.m
        print("asdasdasd "+str(self.xi))
        return self.xi/(self.m-1)

    def move_model(self):
        result=0
        num=self.calculate_ri()
        if num >= 0 and num <=0.333333:
            result=0
        elif num >=0.34 and num <= 0.6666:
            result=1
        elif num >=0.7 and num <=1:
            result=-1
        return result

#f=RandomNumber()
#for i in range(0,225):
#    num=f.move_model()
#    print(num)