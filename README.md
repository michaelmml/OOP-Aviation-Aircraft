# OOP Aviation & Aircraft
Object-oriented programming in aviation; graphs and network optimisation for routes and aircraft utilisation / maintenance forecasting

## Table of Contents
* [Maintenance Cycle Modelling](#maintenance-cycle-modelling)
* [Routes and Networks](#routes-and-networks)

## Maintenance Cycle Modelling
The value of an aircraft over time is heavily dependent on its maintenance condition and therefore the cost of the maintenance events. This is aggregated based on the main components and % life with respect to each flight cycle (FC) / flight hour (FH) / age limits. Input at an asset class level for general costs and component limits and also at an asset-specific level for current status. They drive flyforward on - Airframe, APU, Landing Gear, Engine Performance Restoration x 2 and LLPs x 2. LLPs can be further broken down into several groupings with slightly different cycle limits.

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

On a component basis, to generate the maintenance adjustment an accurate assessment of 1) where each major maintenance event is relative to their last and next shop visit, and 2) what percentage of its next shop visit cost is remaining. For 1), this is determined by the aircraft operation which is a projection of future monthly FH and FC and 2) event cost is based on aircraft technical specifications corresponding to the component and data published by OEMs regarding costs.

An aircraft’s half-life adjustment value can be quantified using the following equation. This utility cycle follows a saw-tooth pattern.

**Adjustment from Half-Life = (Mtx Event % Life Remaining – 50%) * (Mtx Event Cost)**

The half-life basis assumes that the airframe, engines, landing gear and all major components are half-way between major overhauls and that any life-limited part (for example an engine disk) has used up half of its life.

![flyforwards](https://user-images.githubusercontent.com/84533632/123513884-a0b3d080-d687-11eb-9e3a-1d06bfd4bcfa.png)

With additional expansion of the model to break down LLPs by three cycle limit groups.

![flyforwards](https://user-images.githubusercontent.com/84533632/123546838-3fa6fe00-d756-11eb-9b3d-c2f8495edc3d.png)
