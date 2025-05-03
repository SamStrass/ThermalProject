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

    #Mass flow calcs
    m_ratio = (s3.h-s2.h)/(s8.h-s5.h)
    m_hpl = (-Q_out)/(s6.h-s7.h)
    m_lpl = m_hpl/m_ratio

    #Compressor Work Calcs
    W_cmp1 = 1*m_lpl*(s2.h-s1.h)
    W_cmp2 = 1*m_hpl*(s6.h-s5.h)
    W_cyc = W_cmp1+W_cmp2

    #Energy transfer calcs
    Q_in = m_lpl*(s1.h-s4.h)
    beta = abs(Q_out/W_cyc)
    
    #Debug Printing
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

    
    return [beta, m_ratio, m_hpl, m_lpl, W_cmp1, W_cmp2, W_cyc]
    

beta = loop(Plow, Phx, Phx, Phigh, fluid_LPL, fluid_HPL)
print(loop(Plow, 5*10**5, 5*10**5, Phigh, fluid_LPL, fluid_HPL))
print(loop(Plow, 6*10**5, 6*10**5, Phigh, fluid_LPL, fluid_HPL))
print(loop(Plow, 7*10**5, 7*10**5, Phigh, fluid_LPL, fluid_HPL))
print(loop(Plow, 8*10**5, 8*10**5, Phigh, fluid_LPL, fluid_HPL))
print(loop(Plow, 9.9*10**5, 9.9*10**5, Phigh, fluid_LPL, fluid_HPL))



Phx = np.linspace(4.1*10**5, 9.9*10**5,500)

n = []          #Beta
mr = []         #Mass ratio
mhpl = []       #Mass Flow (High pressure)
mlpl = []       #Mass Flow (Low pressure)
wc1 = []        #Work in compressor 1
wc2 = []        #Work in compressor 1
wtot = []       #Work in cycle
for x in Phx:
    n.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[0])
    mr.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[1])
    mhpl.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[2])
    mlpl.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[3])
    wc1.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[4])
    wc2.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[5])
    wtot.append(loop(Plow, x, x, Phigh, fluid_LPL, fluid_HPL)[6])

Phx_bar =[]
for x in Phx:
    Phx_bar.append(x*(10**-5))

#Plot COP Vs pressure
plt.figure(1)
plt.plot(Phx_bar, n)
plt.xlabel("Pressure (Bar)")
plt.ylabel("COP")
plt.title("Beta vs Pressure of Intermediate Heat Exchanger")
plt.savefig("COP",dpi = 300, transparent = True)

#Plot mass ratio vs pressure
plt.figure(2)
plt.plot(Phx_bar, mr)
plt.xlabel("Pressure (Bar)")
plt.ylabel("Mass Ratio (Ammonia/Propane)")
plt.title("Mass Ratio vs Pressure of Intermediate Heat Exchanger")
plt.savefig("MassRatio",dpi = 300, transparent = True)

#Plot mass flow (high pressure loop) vs pressure
plt.figure(3)
plt.plot(Phx_bar, mhpl)
plt.xlabel("Pressure (Bar)")
plt.ylabel("Mass Flow Rate (kg/s)")
plt.title("Mass Flow in High Pressure Loop vs Pressure of Intermediate Heat Exchanger")
plt.savefig("MassHPL",dpi = 300, transparent = True)

#Plot mass flow (low pressure loop) vs pressure
plt.figure(4)
plt.plot(Phx_bar, mlpl)
plt.xlabel("Pressure (Bar)")
plt.ylabel("Mass Flow Rate (kg/s)")
plt.title("Mass Flow in Low Pressure Loop vs Pressure of Intermediate Heat Exchanger")
plt.savefig("MassLPL",dpi = 300, transparent = True)

#Plot low pressure compressor work vs pressure
plt.figure(5)
plt.plot(Phx_bar, wc1)
plt.xlabel("Pressure (Bar)")
plt.ylabel("Power (kW)")
plt.title("Work in Compressor 1 vs Pressure of Intermediate Heat Exchanger")
plt.savefig("w1",dpi = 300, transparent = True)

#Plot high pressure compressor work vs pressure
plt.figure(6)
plt.plot(Phx_bar, wc2)
plt.xlabel("Pressure (Bar)")
plt.ylabel("Power (kW)")
plt.title("Work in Compressor 2 vs Pressure of Intermediate Heat Exchanger")
plt.savefig("w2",dpi = 300, transparent = True)

#Plot total compressor work vs pressure
plt.figure(7)
plt.plot(Phx_bar, wtot)
plt.xlabel("Pressure (Bar)")
plt.ylabel("Power (kW)")
plt.title("Work in Cycle vs Pressure of Intermediate Heat Exchanger")
plt.savefig("wtot",dpi = 300, transparent = True)


def getMax(arr, m=0):
    '''
    This function takes in an array and outputs the maximum of that array.
    '''
    if arr == []:
        return m
    if arr[0] > m:
        return getMax(arr[1:],arr[0])
    return getMax(arr[1:],m)

def getIndex(n,arr, i=0):
    '''
    This funciotn takes in an array and a value and outputs the index of that value in the array.
    It returns -1 if the value is not in the array.
    '''
    if len(arr) < 1:
        return -1
    if n == arr[0]:
        return i
    return getIndex(n,arr[1:],i+1)
    
T_hot = 25+273.15
T_cold = 0+273.15
beta_max = T_hot/(T_hot-T_cold)
print("Theoretical Beta Max: ", beta_max)
maxVal = getMax(n)
print("Max COP: ",maxVal)
i = getIndex(maxVal,n)
print("Pressure at Max COP: ",Phx[n.index(maxVal)])


with open("data.csv","w") as f:
    f.write("Pressure,Beta,massratio,comp1,comp2,wtot\n")

    for i in range(len(Phx)):
        wstring = str(Phx[i])+","+str(n[i])+","+str(mr[i])+","+str(wc1[i])+","+str(wc2[i])+","+str(wtot[i])+"\n"
        f.write(wstring)