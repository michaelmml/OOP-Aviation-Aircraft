# OOP Aviation & Aircraft
Object-oriented programming in aviation; graphs and network optimisation for routes and aircraft utilisation / maintenance forecasting

## Table of Contents
* [Maintenance Cycle Modelling](#maintenance-cycle-modelling)
* [Routes and Networks](#routes-and-networks)

## Maintenance Cycle Modelling
Aggregate of the following components and % life based on flight cycle (FC) or flight hour (FH) limits. Input at an asset class level for general pricing and component limits and also at an asset-specific level for current status of components. They driven flyforward on the five key components - Airframe, APU, Landing Gear, Engine Performance Restoration x 2 and LLPs x 2.

```
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
```

![flyforwards](https://user-images.githubusercontent.com/84533632/123513884-a0b3d080-d687-11eb-9e3a-1d06bfd4bcfa.png)
