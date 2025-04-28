from numpy import *
from matplotlib.pyplot import *
import CoolProp.CoolProp as CP


specific_volume = linspace (0.001, 3, 100)
density = 1/specific_volume


class State:
    #With Mass/Mass Flow
    
    
    def __init__(self, P1="P", V1=10**5, P2="T", V2=373, f="water"):
        self.fluid = f
        self.p =  CP.PropsSI("P",P1,V1,P2,V2,f)                         #Pressure in Pa
        self.t = CP.PropsSI("T",P1,V1,P2,V2,f)                          #Temperature in K
        self.sv =  (1/CP.PropsSI("D",P1,V1,P2,V2,f))/1000               #Specific Volume in kj/kg
        self.u = CP.PropsSI("U",P1,V1,P2,V2,f)/1000                     #Internal Energy in kJ/kg
        self.h = CP.PropsSI("H",P1,V1,P2,V2,f)/1000                     #Enthalpy in kJ/kg
        self.s = CP.PropsSI("S",P1,V1,P2,V2,f)/1000                     #Entropy in kJ/kg * K
        self.x = CP.PropsSI("Q",P1,V1,P2,V2,f)                          #Quality (m_vap / m_tot)%
        self.phase = CP.PhaseSI("P", self.p, "T", self.t, self.fluid)   #Phase (liquid/gas)


    def getPhase(self):
        return CP.PhaseSI("P", self.p, "T", self.t, self.fluid)
    

    def __str__(self):
        output = ("Fluid: " + str(self.fluid) + 
                #   "\nPhase: " + self.getPhase() + 
                  "\nPressure: "+ str(self.p) + " Pa" +
                  "\nTempreature: "+ str(self.t-273.15) + " C" + 
                  "\nSpecific Volume: " + str(self.sv) + " kg/m^3" + 
                  "\nInternal Energy: " + str(self.u) + " kj/kg" + 
                  "\nEnthalpy: " + str(self.h) + " kj/kg" + 
                  "\nEntropy: " + str(self.s) + " kj/kg * K" + 
                  "\nQuality: " + str(self.x) + "%")
        return output

def compressor_eff(s1,s2):
    s2s = State("P", s2.p, "S", s1.s, s1.fluid)
    eff = (s1.h-s2.h)/(s1.h-s2s.h)
    return eff



# s1 = State("P", 120, "T", 10+273.15, "air")
# s2 = State("P", 1000e3, "T", 273.527+273.15, "air")
# print(s2.h)
# print(s1.getPhase())
# print((s1.h - s2.h)*10**-3)
# print(compressor_eff(s1,s2))
