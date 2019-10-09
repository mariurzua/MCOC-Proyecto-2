import math
from matplotlib.pylab import *

#Unidades base son SI
_kg = 1.
_s = 1.
_m = 1.
_mm = 1e-3*_m
_cm = 1e-2*_m
_gr = 1e-3*_kg

vfx = 10.0*_m/_s 
vfy = 0.0*_m/_s

Nparticulas = 3

g = 9.81*_m/_s**2
d = 1*_mm
rho_particula = 2700.*_kg/(_m**3)
rho_agua = 1000.*_kg/(_m**3)
Cd = 0.47							#para una particula
Cl = 0.2
Cm = 0.2
Rp = 73
A = pi*(d/2)**2
V = (4./3.)*pi*(d/2)**3
m = rho_particula*V
x0 = zeros((Nparticulas*4),dtype=double)
for i in range(Nparticulas):
	x0[4*i+1] = random()*d*20
	x0[4*i+2:(4*i+4)] = rand(2)*d*50


#x0 = array([0.,0.1], dtype = double)
x1 = array([0.,0.15], dtype = double)

v0 = array([0.5,0.2], dtype = double)
v1 = array([0.3,0.2], dtype = double)
#Inicializar en x0

dt = 0.001*_s 		#paso de tiempo
tmax = 2.*_s 		#tiempo maximo de simulacion
ti = 0.0*_s			#tiempo actual

W = array([0.,-m*g])
fB = array([0,rho_agua*V*g])

t = arange(0,tmax,dt)
Nt = len(t)

norm = lambda v: sqrt(dot(v,v))

k_penal = 10000*0.5*Cd*rho_agua*A*norm(vfx)/(1*_mm)



def velocity_field(x):
	z = x[1]/d
	if z > (1./30.):
		vf = 2.439*log(30*z)
	else:
		vf = 0
	return array([vf,0])

def particula(z,t):
	zp = zeros(4*Nparticulas)
	for i in range(Nparticulas):
		xi = z[4*i:(4*i+2)]
		vi = z[4*i+2:(4*i+4)]
		vf = velocity_field(xi)
		vrel = vf - vi
		fD = (0.5*Cd*rho_agua*norm(vrel)*A)*vrel 
		vt = velocity_field(xi + d/2)
		vrt = vt - vi
		vb = velocity_field(xi - d/2)
		vrb = vb - vi 
		fL = array([0.,0.5*rho_agua*A*Cl*(norm(vrt)**2-norm(vrb)**2)], dtype = double) 
		Fi = W  + fB + fL + fD

		if xi[1] <0:
			Fi[1] += -k_penal*xi[1]
		for j in range(Nparticulas):
			xj = z[4*j:(4*j+2)]
			vj = z[4*j+2:(4*j+4)]
			if i>j:
				rij = norm(xi-xj)
				print rij
				if rij < d:
					print "adentro"
					tetha = arctan2(((xi[1]-xj[1])**2)**0.5,((xi[1]-xj[0])**2)**0.5)*180/math.pi
					Fi += array([k_penal*(d-rij)*cos(tetha),k_penal*rij*sin(tetha)])
					Fj = -Fi
					zp[4*j+2:4*j+4] += Fj/m
					zp[4*i+2:4*i+4] += Fi/m
		zp[4*i:4*i+2] = vi
		zp[4*i+2:4*i+4] = Fi/m
	#for i in range(Nparticulas):
	#	xi = z[4*i:(4*i+2)]
	#	vi = z[4*i+2:(4*i+4)]
	#	for j in range(Nparticulas):
	#		xj = z[4*j:(4*j+2)]
	#		vj = z[4*j+2:(4*j+4)]
	#		if i>j:
	#			rij = norm(xi-xj)
	#			print rij
	#			if rij < d:
	#				tetha = arctan2(((xi[1]-xj[1])**2)**0.5,((xi[1]-xj[0])**2)**0.5)*180/math.pi
	#				Fi += array([k_penal*rij*cos(tetha),k_penal*rij*sin(tetha)])
	#				Fj = -Fi
	#				zp[4*j+2:4*j+4] += Fj/m
	#				zp[4*i+2:4*i+4] += Fi/m

	return zp
from scipy.integrate import odeint

print "INTEGRANDO"
z=odeint(particula,x0,t)
print "Finalizado"
x0 = z[:,0:2]
x1 = z[:,4:6]
x2 = z[:,8:10]
v=z[:,2:]


figure()

plot(x0[:,0],x0[:,1])
plot(x1[:,0],x1[:,1])
plot(x2[:,0],x2[:,1])

#figure()
#subplot(2,1,1)
#plot(t,x[:,0],label="x")
#plot(t,x[:,1],label="y")
#subplot(2,1,2)
#plot(t,v[:,0],label="vx")
#plot(t,v[:,0],label="vy")

show()