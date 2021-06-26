"""
def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x] #First, we check if the input, which will be the
                       #dictionary key, exists in the dictionary. If the key is present we return the value
                       #corresponding to the input/key
    return helper
"""


# After having executed fib = memoize(fib) fib points to the body of the helper function, which had been returned by
# memoize. We can also perceive that the code of the original fib function can only be reached via the "f" function
# of the helper function from now on. There is no other way anymore to call the original fib directly, i.e. there is
# no other reference to it. The decorated Fibonacci function is called in the return statement return fib(n-1) + fib(
# n-2), this means the code of the helper function which had been returned by memoize:

class Memo:

    # Create class storing function results and index
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    # Argument is the k for the function fn
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.fn(*args)

        return self.memo[args]


@Memo
def Fib(k):
    if k <= 1: return 0
    if k == 2: return 1
    return Fib(k - 1) + Fib(k - 2)


# Fib = Memo(Fib) essentially the decorator
print(Fib(20))
print(Fib.__dict__)

# Objects
# Asset type threshold / cost assumptions
# 6 yr C Check / 12 yr Check / APU / Landing Gear / EPR / LLP
costs = [100000, 1000000, 300000, 400000, 5300000, 8400000]
threshold = [[0,0,0,0,0,0],[6, 144, 9500, 20000, 20000, 25000], [6, 144, 9500, 20000, 20000, 22000],
             [6, 144, 9500, 20000, 20000, 22000], [6, 144, 9500, 20000, 20000, 22000],
             [6, 144, 9500, 20000, 20000, 22000], [6, 144, 9500, 20000, 20000, 22000],
             [6, 144, 9500, 20000, 20000, 22000], [6, 144, 9500, 20000, 20000, 22000]]

# Building OOP on aircraft utilisation depends on what to create the class ON
# E.g. a class of a particular aircraft and its utilisation status at certain times being the object, as is below
# Or by different aircraft types, which gets complicated due to how dynamic the attributes are over time

import matplotlib.pyplot as plt
import math


def cycle(x,t):
    metric = 0
    for j in range(5):
        metric += threshold[j][x]
        if metric > t:
            return j


class UtilisationGeneric:

    def __init__(self, age_ori, fh, fc, freq):
        self.age_ori = age_ori
        self.fh_m = fh * 30.5 * freq
        self.fc_m = fc * 30.5 * freq


class AircraftUtilisation:
    # 6c,12c,apu,ldg,eng_epr,llp

    def __init__(self, UtilisationGeneric, age, fh_cum, fc_cum, last1, last2, last3, last4, last5):
        self.age = age
        self.UtilisationGeneric = UtilisationGeneric
        self.fh_cum = fh_cum
        self.fc_cum = fc_cum

        self.r1_cumevent = last1
        self.r2_cumevent = last2
        self.r3_cumevent = last3
        self.r4_cumevent = last4
        self.r5_cumevent = last5

        self.r1 = cycle(1, last1)
        self.r2 = cycle(2, last2)
        self.r3 = cycle(3, last3)
        self.r4 = cycle(4, last4)
        self.r5 = cycle(5, last5)

        self.r1_eventdate = 0
        self.r2_eventdate = 0
        self.r3_eventdate = 0
        self.r4_eventdate = 0
        self.r5_eventdate = 0

    def utilise(self):
        self.age += 1
        self.fh_cum = self.UtilisationGeneric.fh_m + self.fh_cum
        self.fc_cum = self.UtilisationGeneric.fc_m + self.fc_cum

        if self.age > 25*12:
            return

        if self.age - self.r1_cumevent > threshold[self.r1][1]:
            self.ratio_1 = 0
            self.r1_cumevent += threshold[self.r1][1]
            self.r1_eventdate = self.age
            self.r1 += 1
        else:
            self.ratio_1 = (self.age - self.r1_cumevent) / threshold[self.r1][1]

        if self.fh_cum - self.r2_cumevent > threshold[self.r2][2]:
            self.ratio_2 = 0
            self.r2_cumevent += threshold[self.r2][2]
            self.r2_eventdate = self.age
            self.r2 += 1
        else:
            self.ratio_2 = (self.fh_cum - self.r2_cumevent) / threshold[self.r2][2]

        if self.fc_cum - self.r3_cumevent > threshold[self.r3][3]:
            self.ratio_3 = 0
            self.r3_cumevent += threshold[self.r3][3]
            self.r3_eventdate = self.age
            self.r3 += 1
        else:
            self.ratio_3 = (self.fc_cum - self.r3_cumevent) / threshold[self.r3][3]

        if self.fh_cum - self.r4_cumevent > threshold[self.r4][4]:
            self.ratio_4 = 0
            self.r4_cumevent += threshold[self.r4][4]
            self.r4_eventdate = self.age
            self.r4 += 1
            self.age += 3
        else:
            self.ratio_4 = (self.fh_cum - self.r4_cumevent) / threshold[self.r4][4]

        if self.fh_cum > self.r5 * threshold[self.r5][5]:
            self.ratio_5 = 0
            self.r5_cumevent += threshold[self.r5][5]
            self.r5_eventdate = self.age
            self.r5 += 1
            self.age += 6
        else:
            self.ratio_5 = (self.fh_cum - self.r5_cumevent) / threshold[self.r5][5]


class AircraftComp:
    escalation = 0.02

    def __init__(self, AircraftUtilisation):
        self.AircraftUtilisation = AircraftUtilisation

    @classmethod
    def about(cls):
        print("This class is instances of a specific aircraft's maintenance status.")

    def flyforwardcalc(self):
        self.twelvec = (costs[1]*(1+AircraftComp.escalation)**(self.AircraftUtilisation.r1_eventdate/12)) * (0.5 - self.AircraftUtilisation.ratio_1)
        self.apu = (costs[2]*(1+AircraftComp.escalation)**(self.AircraftUtilisation.r2_eventdate/12)) * (0.5 - self.AircraftUtilisation.ratio_2)
        self.ldg = (costs[3]*(1+AircraftComp.escalation)**(self.AircraftUtilisation.r3_eventdate/12)) * (0.5 - self.AircraftUtilisation.ratio_3)
        self.epr = (costs[4]*(1+AircraftComp.escalation)**(self.AircraftUtilisation.r4_eventdate/12)) * (0.5 - self.AircraftUtilisation.ratio_4)
        self.llp = (costs[5]*(1+AircraftComp.escalation)**(self.AircraftUtilisation.r5_eventdate/12)) * (0.5 - self.AircraftUtilisation.ratio_5)
        self.mtx_adj = self.twelvec + self.apu + self.ldg + self.epr + self.llp

# Aircraft / lease specific input
fh = 1.5
fc = 1
frequency = 7
fh_cum_init = 120
fc_cum_init = (fh_cum_init / fh) * fc
age_init = 96
last = 0

# Running flyforwards...
A320 = UtilisationGeneric(age_init, fh, fc, frequency)
MSN1 = AircraftUtilisation(A320, age_init, fh_cum_init, fc_cum_init, last, last, last, last, last)
flyforwards = []
age_profile = []
for i in range(1, 12 * 20):
    MSN1.utilise()
    age_profile.append(MSN1.age)
    MSN1FF = AircraftComp(MSN1)
    MSN1FF.flyforwardcalc()
    x = MSN1FF.mtx_adj
    flyforwards.append(x)

print(flyforwards)

plt.plot(age_profile, flyforwards, 'r', label='FF')
plt.xlabel('Months')
plt.ylabel('$')
plt.legend()
plt.show()


# print(A320.__dict__)
# print(Ryanair.__dict__)
# print(MSN1.__dict__)

# self.r1 = r1
# self.r2 = r2
# self.r3 = r3
# self.r4 = r4
# self.r5 = r5
# self.twelvec = costs[1] * (0.5 - (age / threshold[1]))
# self.apu = costs[2] * (0.5 - (fc_now / threshold[2]))
# self.ldg = costs[3] * (0.5 - (fc_now / threshold[3]))
# self.epr = costs[4] * (0.5 - (fh_now / threshold[4]))
# self.llp = costs[5] * (0.5 - (fh_now / threshold[5]))
# self.mtx_adj = self.twelvec + self.apu + self.ldg + self.epr + self.llp

"""
class Clock(object):

    # Cases of a class with objects starting from a point, and a function (tick) to move attributes of the object along
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds

    def set(self, hours, minutes, seconds=0):
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds

    def tick(self):
        if self.__seconds == 59:
            self.__seconds = 0
            if (self.__minutes == 59):
                self.__minutes = 0
                self.__hours = 0 if self.__hours == 23 else self.__hours + 1
            else:
                self.__minutes += 1;
        else:
            self.__seconds += 1;

    def display(self):
        print("%d:%d:%d" % (self.__hours, self.__minutes, self.__seconds))

    def __str__(self):
        return "%2d:%2d:%2d" % (self.__hours, self.__minutes, self.__seconds)


class Calendar(object):
    months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    def __init__(self, day=1, month=1, year=1900):
        self.__day = day
        self.__month = month
        self.__year = year

    def leapyear(self, y):
        if y % 4:
            # not a leap year
            return 0;
        else:
            if y % 100:
                return 1;
            else:
                if y % 400:
                    return 0
                else:
                    return 1;

    def set(self, day, month, year):
        self.__day = day
        self.__month = month
        self.__year = year

    def get():
        return (self, self.__day, self.__month, self.__year)

    def advance(self):
        months = Calendar.months
        max_days = months[self.__month - 1]
        if self.__month == 2:
            max_days += self.leapyear(self.__year)
        if self.__day == max_days:
            self.__day = 1
            if (self.__month == 12):
                self.__month = 1
                self.__year += 1
            else:
                self.__month += 1
        else:
            self.__day += 1

    def __str__(self):
        return str(self.__day) + "/" + str(self.__month) + "/" + str(self.__year)


class CalendarClock(Clock, Calendar):

    def __init__(self, day, month, year, hours=0, minutes=0, seconds=0):
        Calendar.__init__(self, day, month, year)
        Clock.__init__(self, hours, minutes, seconds)

    def __str__(self):
        return Calendar.__str__(self) + ", " + Clock.__str__(self)


if __name__ == "__main__":
    x = CalendarClock(24, 12, 57)
    print(x)
    for i in range(1000):
        x.tick()
    for i in range(1000):
        x.advance()
    print(x)

"""