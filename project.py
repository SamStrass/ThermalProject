from state import State
import numpy as np
from matplotlib import pyplot as plt


'''
Stuff Needed
    - Mass ratio
    - power in each compressor
    - total power
    - COP

    - Difference in energy required between cascade vs single
'''

#Low Pressure Loop
fluid_LPL = "ammonia"
Plow = 4*10**5

#Intermediate Properties
Phx = 6*10**5


#High Pressure Loop
Phigh = 10*10**5
fluid_HPL = "propane"
Q_out = -150


def loop(P1, P2, P5, P6, lpl_fluid, hpl_fluid):
    #Low Pressure Loop States
    global s1;global s2;global s3;global s4;global s5;global s6;global s7;global s8
    s1 = State("P", P1, "Q", 1, lpl_fluid)
    s2 = State("P", P2, "S", s1.s*1000, lpl_fluid)
    s3 = State("P", P2, "Q", 0, lpl_fluid)
    s4 = State("H", s3.h*1000, "P", P1, lpl_fluid)
    
    #High Pressure Loop States
    s5 = State("P", P5, "Q", 1, hpl_fluid)
    s6 = State("P", P6, "S", s5.s*1000, hpl_fluid)
    s7 = State("P", P6, "Q", 0, hpl_fluid)
    s8 = State("H", s7.h*1000, "P", P5, hpl_fluid)

    m_ratio = (s3.h-s2.h)/(s8.h-s5.h)
    m_hpl = (-Q_out)/(s6.h-s7.h)
    m_lpl = m_hpl/m_ratio

    W_cmp1 = 1*m_lpl*(s2.h-s1.h)
    W_cmp2 = 1*m_hpl*(s6.h-s5.h)
    W_cyc = W_cmp1+W_cmp2

    Q_in = m_lpl*(s1.h-s4.h)
    beta = Q_in/W_cyc
    # print(beta)

    # print(s1.h)

    # print(m_ratio)
    # print(m_hpl)
    # print(m_lpl)
    # print(s1.x)
    # print(s1.s)
    # print(s2.h,s1.h, "\n",s6.h,s5.h)
    # print(s5.s)
    # print("W comp1: ", W_cmp1)
    # print("W comp2: ", W_cmp2)
    # print(s7.t-273.15)

    

    n_actual = abs((Q_out)/(W_cmp1+W_cmp2))
    # print(abs(n_actual))
    return [n_actual, m_ratio,W_cmp1,W_cmp2,W_cyc]
    

beta = loop(Plow, Phx, Phx, Phigh, fluid_LPL, fluid_HPL)
print("Beta act: ",beta)
Phx = np.linspace(4.1*10**5, 9.9*10**5,500)

n = []          #Beta
mr = []         #Mass ratio
wc1 = []        #Work in compressor 1
wc2 = []        #Work in compressor 1
wtot = []       #Work in cycle
for x in Phx:
    n.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[0])
    mr.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[1])
    wc1.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[2])
    wc2.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[3])
    wtot.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[4])


plt.figure(1)
plt.plot(Phx, n)
plt.xlabel("Pressure(Pa)")
plt.ylabel("COP")
plt.title("Beta vs Pressure of Intermediate Heat Exchanger")
plt.savefig("COP",dpi = 300, transparent = True)

plt.figure(2)
plt.plot(Phx, mr)
plt.xlabel("Pressure(Pa)")
plt.ylabel("Mass Ratio (Ammonia/Propane)")
plt.title("Mass Ratio vs Pressure of Intermediate Heat Exchanger")
plt.savefig("MassRatio",dpi = 300, transparent = True)

plt.figure(3)
plt.plot(Phx, wc1)
plt.xlabel("Pressure(Pa)")
plt.ylabel("Energy (kJ)")
plt.title("Work in Compressor 1 vs Pressure of Intermediate Heat Exchanger")
plt.savefig("w1",dpi = 300, transparent = True)

plt.figure(4)
plt.plot(Phx, wc2)
plt.xlabel("Pressure(Pa)")
plt.ylabel("Energy (kJ)")
plt.title("Work in Compressor 2 vs Pressure of Intermediate Heat Exchanger")
plt.savefig("w2",dpi = 300, transparent = True)

plt.figure(5)
plt.plot(Phx, wtot)
plt.xlabel("Pressure(Pa)")
plt.ylabel("Energy (kJ)")
plt.title("Work in Cycle vs Pressure of Intermediate Heat Exchanger")
plt.savefig("wtot",dpi = 300, transparent = True)


def getMax(arr, m=0):
    if arr == []:
        return m
    if arr[0] > m:
        return getMax(arr[1:],arr[0])
    return getMax(arr[1:],m)

def getIndex(n,arr, i=0):
    if len(arr) > 1:
        return -1
    if n == arr[0]:
        return i
    return getIndex(n,arr[1:],i+1)
    
# print(n)
T_hot = 25+273.15
T_cold = 0+273.15
beta_max = T_hot/(T_hot-T_cold)
print("Beta Max = ", beta_max)
maxVal = getMax(n)
print(maxVal)
i = getIndex(maxVal,n)
print(i)
print(Phx[n.index(maxVal)])
