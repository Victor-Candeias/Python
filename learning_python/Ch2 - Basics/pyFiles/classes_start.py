#
# Example file for working with classes
# LinkedIn Learning Python course by Joe Marini
#

class Vehicle():
    #constructor
    def __init__(self, bodystyle):
        self.bodystyle = bodystyle
        
    def drive(self, speed):
        self.mode = "driving"
        self.speed = speed
        
    def drivingsense(self, sense):
        self.sense = sense
        
class Car(Vehicle):
    def __init__(self, enginetype):
        super().__init__("Car")
        
        self.wheels = 4
        self.doors = 4
        self.enginetype = enginetype
        
    def drive(self, speed):
        super().drive(speed)
        return ("Driving ny ", self.enginetype, "car at", self.speed)
        
    def drivingsense(self, sense):
        super().drivingsense(sense)
        
        return self.sense
    
class Motorcycle(Vehicle):
    def __init__(self, enginetype, hassidecar):
        super().__init__("Motorcycle")
        
        if (hassidecar):
            self.wheels = 3
        else:
            self.wheels = 2
            
        self.doors = 0
        self.enginetype = enginetype
        
    def drive(self, speed):
        super().drive(speed)
        return ("Driving ny ", self.enginetype, "motorcycle at", self.speed)
        
    def drivingsense(self, sense):
        super().drivingsense(sense)
        
        return self.sense
        
car1 = Car("gas")
car2 = Car("electric")
mc1 = Motorcycle("gas", True)

print(mc1.wheels)
print(car1.enginetype)
print(car2.doors)
print(car1.drive(30))
print(car2.drive(50))
print(mc1.drive(100))

print(car1.drivingsense("right"))
print(car2.drivingsense("left"))
print(mc1.drivingsense("up"))
        