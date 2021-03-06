### Object Oriented Programming on Aircraft Maintenance Projections

### Asset type threshold / cost assumptions
### 6 yr C Check / 12 yr Check / APU / Landing Gear / EPR / LLP
costs = [100000, 1000000, 300000, 400000, 5300000, 8400000]
threshold = [[0,0,0,0,0,0],[6, 144, 9500, 20000, 20000, 25000], [6, 144, 9500, 20000, 20000, 22000],
             [6, 144, 9500, 20000, 20000, 22000], [6, 144, 9500, 20000, 20000, 22000],
             [6, 144, 9500, 20000, 20000, 22000], [6, 144, 9500, 20000, 20000, 22000],
             [6, 144, 9500, 20000, 20000, 22000], [6, 144, 9500, 20000, 20000, 22000]]

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

### Aircraft / lease specific input
fh = 1.5
fc = 1
frequency = 7
fh_cum_init = 120
fc_cum_init = (fh_cum_init / fh) * fc
age_init = 96
last = 0

### Running flyforwards...
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
