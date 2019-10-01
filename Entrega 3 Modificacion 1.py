from matplotlib.pylab import *

#Unidades base son SI
_kg = 1.
_s = 1.
_m = 1.
_mm = 1e-3*_m
_cm = 1e-2*_m
_gr = 1e-3*_kg

vfx = 10.0*_m/_s 
vfy = 0.1*_m/_s 

x0 = array([0., 1.*_mm], dtype = double)
v0 = array([1., 1.], dtype = double)

xi = x0#zeros(2, dtype = double)		#posicion actual
vi = v0#zeros(2, dtype = double)		#velocidad actual
ximl = zeros(2, dtype = double)		#posicion siguiente
viml = zeros(2, dtype = double)		#velocidad siguiente

g = 9.81*_m/_s**2
d = 1*_mm
rho_particula = 2700.*_kg/(_m**3)
rho_agua = 1000.*_kg/(_m**3)
Cd = 0.47							#para una particula

A = pi*(d/2)**2
V = (4./3.)*pi*(d/2)**3
m = rho_particula*V

#Inicializar en x0

dt = 0.001*_s 		#paso de tiempo
tmax = 2.*_s 		#tiempo maximo de simulacion
ti = 0.0*_s			#tiempo actual

W = array([0.,-m*g])
fB = array([0,rho_agua*V*g])

t = arange(0,tmax,dt)
Nt = len(t)

norm = lambda v: sqrt(dot(v,v))

k_penal = 1000*0.5*Cd*rho_agua*A*norm(v0)/(1*_mm)

def particula(z,t):
	xi = z[:2]
	vi = z[2:]
	vf = array([vfx,vfy])
	vrel = vf - vi
	fD = (0.5*Cd*rho_agua*norm(vrel)*A)*vrel
	Fi = W + fD + fB

	if xi[1] <0:
		Fi[1] += -k_penal*xi[1]

	zp = zeros(4)
	zp[:2] = vi
	zp[2:] = Fi/m
	return zp

from scipy.integrate import odeint
z0 = zeros(4)
z0[:2] = x0
z0[2:] = v0
z = odeint(particula,z0,t)
x = z[:,:2]
v = z[:,2:]

figure()
plot(x[:,0],x[:,1])
ylim([0,10*_mm])

#figure()
#subplot(2,1,1)
#plot(t,x[:,0],label="x")
#plot(t,x[:,1],label="y")
#subplot(2,1,2)
#plot(t,v[:,0],label="vx")
#plot(t,v[:,0],label="vy")

show()