# OOP Aviation & Aircraft
Object-oriented programming in aviation; graphs and network optimisation for routes and aircraft utilisation / maintenance forecasting

## Table of Contents
* [Maintenance Cycle Modelling](#maintenance-cycle-modelling)

## Maintenance Cycle Modelling
Aggregate of the following components and % life based on flight cycle (FC) or flight hour (FH) limits.

```
    def utilise(self):
        self.age += 1
        self.fh_cum = self.UtilisationGeneric.fh_m + self.fh_cum
        self.fc_cum = self.UtilisationGeneric.fc_m + self.fc_cum

        if self.age > 25*12:
            return

        if self.age > self.r1 * threshold[self.r1 - 1][1]:
            self.ratio_1 = (self.age / threshold[self.r1 - 1][1]) - self.r1
            self.r1 += 1
            self.age += 1
        else:
            self.ratio_1 = (self.age / threshold[self.r1 - 1][1]) - self.r1 + 1

        if self.fc_cum > self.r2 * threshold[self.r2 - 1][2]:
            self.ratio_2 = (self.fc_cum / threshold[self.r2 - 1][2]) - self.r2
            self.r2 += 1
            self.age += 1
        else:
            self.ratio_2 = (self.fc_cum / threshold[self.r2 - 1][2]) - self.r2 + 1

        if self.fc_cum > self.r3 * threshold[self.r3 - 1][3]:
            self.ratio_3 = (self.fc_cum / threshold[self.r3 - 1][3]) - self.r3
            self.r3 += 1
            self.age += 1
        else:
            self.ratio_3 = (self.fc_cum / threshold[self.r3 - 1][3]) - self.r3 + 1
```
