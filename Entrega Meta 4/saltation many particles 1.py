
from matplotlib.pylab import *
import random
#Unidades base son SI
_kg = 1.
_s = 1.
_m = 1.
_mm = 1e-3*_m
_cm = 1e-2*_m
_gr = 1e-3*_kg


Nparticulas = 5

g = 9.81*_m/_s**2
d = 0.15*_mm
rho_particula = 2650.*_kg/(_m**3) 	 #Densidad obtenida de Nino and Garcia  (1994)
rho_agua = 1000.*_kg/(_m**3)
Cd = 0.47							 #para una particula
Cl = 0.2
Cm = 0.5
R = (rho_particula/rho_agua)-1
alpha = 1/(1 + R + Cm)
ustar = 0.14  # ustar obtenido de Nino and Garcia (1994)

A = pi*(d/2)**2
V = (4./3.)*pi*(d/2)**3
m = rho_particula*V
W = array([0.,m*g])

ihat = array([1,0])
jhat = array([0,1])

x0 = 10*d*rand(Nparticulas)
y0 = 3*d*rand(Nparticulas) + d
vx0 = rand(Nparticulas)/2
vy0 = rand(Nparticulas)/2


#Inicializar en x0

dt = 0.0001*_s 		#paso de tiempo
tmax = 2.*_s 		#tiempo maximo de simulacion
ti = 0.0*_s			#tiempo actual

t = arange(0,tmax,dt)
Nt = len(t)

norm = lambda v: sqrt(dot(v,v))


def velocity_field(x):
	z = x[1]/d
	if z > (1./30.):
		vf = ustar*log(30*z)/0.41
		vf = vf * (vf>0)
	else:
		vf = 0
	return array([vf,0])

vfx = velocity_field([0,10*d])[0]
k_penal = 0.5*Cd*rho_agua*A*norm(vfx)**2/(d/20)

def fuerzas_hidrodinamicas(x,v,d,area,masa):

	xtop = x + (d/2)*jhat
	xbot = x - (d/2)*jhat
	vf = velocity_field(x + 0*jhat)

	vrelf_top = abs(velocity_field(xtop)[0])
	vrelf_bot = abs(velocity_field(xbot)[0])

	vrel = vf - v

	Cd = 0.47
	fD = (0.5*Cd*alpha*rho_agua*norm(vrel)*area)*vrel

	fL = (0.5*Cl*alpha*rho_agua*(vrelf_top - vrelf_bot)*A)*vrel[0]*jhat
	fW = (-masa*g)*jhat

	Fh = fW + fD + fL

	return Fh

def fondo(x):
	x_mod_d = (x % d) - d/2
	y = sqrt((d/2)**2 - x_mod_d**2)
	return y

def particula(z,t):
	zp = zeros(4*Nparticulas)
	
	for i in range(Nparticulas):
		xi = z[4*i:(4*i+2)]
		vi = z[4*i+2:(4*i+4)]
		
		F_h = fuerzas_hidrodinamicas(xi,vi,d,A,m)

		if xi[1] < fondo(xi[0]):
			F_h[1] += -k_penal*xi[1]
		
		zp[4*i:(4*i+2)] = vi
		zp[4*i+2:(4*i+4)] = F_h/m

	for i in range(Nparticulas):
		xi = z[4*i:(4*i+2)]
		for j in range(Nparticulas):
			if i>j:
				xj = z[4*j:(4*j+2)]
				vj = z[4*j+2:(4*j+4)]
				rij = norm(xj-xi)
				if rij < (d):
					tetha = arctan2(((xi[1]-xj[1])**2)**0.5,((xi[1]-xj[0])**2)**0.5)*180/math.pi
					Fi = -array([k_penal*(d-rij)*cos(tetha),k_penal*rij*sin(tetha)])
					Fj = - Fi
					zp[4*j+2:4*j+4] += Fj/m
					zp[4*i+2:4*i+4] += Fi/m
	

	return zp

from scipy.integrate import odeint

print "INTEGRANDO"



z0 = zeros (4*Nparticulas)
z0[0::4] = x0 
z0[1::4] = y0
z0[2::4] = vx0 
z0[3::4] = vy0

z=odeint(particula,z0,t)
print "Finalizado"

figure()

for i in range(Nparticulas):
	xi = z[:,4*i]/d
	yi = z[:,4*i+1]/d
	plot(xi,yi)


show()