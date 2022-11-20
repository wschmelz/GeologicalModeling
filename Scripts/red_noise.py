import os
import sys
import numpy
import matplotlib.pyplot as plt
import scipy
from scipy import signal
from scipy import interpolate
backslash = '\\'

wkspc = str(os.getcwd()).replace(backslash,"/") + "/" 

filename = wkspc + "Data/00_LR04.csv"

LR04 = numpy.genfromtxt(filename,delimiter=",")

w1 = numpy.where(LR04[:,0]<=800)[0]
def lag1_cov(y):
    cov = (1./(len(y)-1.))*numpy.sum(((y[0:-1]-numpy.mean(y))*(y[1:]-numpy.mean(y)))/numpy.var(y))
    return cov
	
def red_noise(y):
			
	red_noise_tmp = numpy.zeros(len(y))
	r = lag1_cov(y)

	white_noise = numpy.random.normal(0.,numpy.std(y),len(y))#* numpy.std(y)
	red_noise_tmp[0] =white_noise[0]
	for index_n in range(0,len(red_noise_tmp)-1):
		red_noise_tmp[index_n+1] =  r * red_noise_tmp[index_n] + numpy.sqrt(1.-(r**2.))*white_noise[index_n+1]

	return red_noise_tmp 

#generate a vector, 1000 values from 0 to T

T = numpy.max(LR04[w1,0])
dt = 1.
x = numpy.arange(0,T,dt)
f = scipy.interpolate.interp1d(LR04[w1,0],LR04[w1,1])
a = scipy.signal.detrend(f(x),type="linear")

monte_carlo_i = 5

fig = plt.figure(3)
ax1 = plt.subplot(211)
ax1.plot(a)

for n in range(0,monte_carlo_i):

    a2 = red_noise(a)

    ax1 = plt.subplot(212)
    ax1.plot(a2)

    plt.pause(1)
plt.show()
plt.close()
print(numpy.sum(a**2.)*dt)

N = len(x)

#fft

fft_LR04 = dt * numpy.fft.fft(a)[:int(N/2)]

freq_LR04 = numpy.fft.fftfreq(len(a),d=dt)[:int(N/2)] #fft frequencies

df_fft = freq_LR04[1] - freq_LR04[0]

G_k = numpy.zeros(len(fft_LR04))

G_k = 2.*(numpy.abs(fft_LR04)**2.)
G_k[0] = numpy.abs(fft_LR04[0])**2.
fig = plt.figure(2)
ax1 = plt.subplot(211)

ax1.plot(LR04[w1,0],LR04[w1,1])
ax1.set_xlim(numpy.max(LR04[w1,0]),0)
ax1.grid()
ax1.set_ylabel("d18O")
ax1.set_xlabel("time (ka)")

monte_carlo_i = 10000


output = numpy.zeros((monte_carlo_i,len(freq_LR04)))
output2 = numpy.zeros(monte_carlo_i)
output3 = numpy.zeros((monte_carlo_i,len(a)))

for n in range(0,monte_carlo_i):
	a2 = red_noise(a)
	output3[n,:] = a2
	fft_rn = dt * numpy.fft.fft(a2)[:int(N/2)]
	freq_rn = numpy.fft.fftfreq(len(a2),d=dt)[:int(N/2)] #fft frequencies
	df_rn = freq_rn[1] - freq_rn[0]
	output[n,:] = 2.*(numpy.abs(fft_rn)**2.)
	output[n,0] = numpy.abs(fft_rn[0])**2.
	output2[n] = numpy.sum(output[n,:])*df_rn

G_k_rn = numpy.quantile(output,0.5,axis=0)
G_k_rn_l = numpy.quantile(output,0.025,axis=0)
G_k_rn_h = numpy.quantile(output,0.975,axis=0)

print(numpy.mean(output2))

ax2 = plt.subplot(212)
ax2.plot(freq_LR04,G_k)
ax2.plot(freq_rn,G_k_rn,color='r')
ax2.plot(freq_rn,G_k_rn_h,linewidth=0.5,linestyle=":",color='r')
ax2.plot(freq_rn,G_k_rn_l,linewidth=0.5,linestyle=":",color='r')
ax2.set_xlim(0,numpy.max(freq_LR04))
ax2.set_xlim(0,1/15)
ax2.set_xlabel("cycles per kyr")
ax2.set_ylabel("ESD")

ax2.grid()

plt.tight_layout()

fig = plt.figure(1)
ax1 = plt.subplot(211)
ax1.plot(LR04[w1,0],LR04[w1,1],label="LR04")
ax1.set_xlim(numpy.max(LR04[w1,0]),0)
ax1.set_ylabel("d18O")
ax1.legend()
ax1.grid()

ax2 = plt.subplot(212)
ax2.plot(x,output3[0,:],label="Correlated noise",color="r")
ax2.plot(x,numpy.mean(output3,axis=0),color="k")
ax2.set_xlim(numpy.max(x),0)
ax2.legend()
ax2.grid()
ax2.set_xlabel("time (ka)")


plt.show()