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
ds = (rand(Nparticulas)*16 + 15)*_mm # Diametro obtenido de Nino and Garcia (1994)
rho_particula = 2650.*_kg/(_m**3) #Densidad obtenida de Nino and Garcia  (1994)
rho_agua = 1000.*_kg/(_m**3)
Cd = 0.47							#para una particula
Cl = 0.2
Cm = 0.2
R = (rho_particula/rho_agua)-1
Rp = 73
alpha = (1 + R + Cm)**-1
ustar = 0.2  # ustar obtenido de Nino and Garcia (1994)

x0 = zeros((Nparticulas*4),dtype=double)
for i in range(Nparticulas):
	x0[4*i+1] = random()*ds[i]*10
	x0[4*i+2:(4*i+4)] = rand(2)*ds[i]*5


#x0 = array([0.,0.1], dtype = double)

#Inicializar en x0

dt = 0.001*_s 		#paso de tiempo
tmax = 2.*_s 		#tiempo maximo de simulacion
ti = 0.0*_s			#tiempo actual

t = arange(0,tmax,dt)
Nt = len(t)

norm = lambda v: sqrt(dot(v,v))

k_penal = 100000*0.5*Cd*rho_agua*0.1*norm(vfx)/(1*_mm)



def velocity_field(x,d):
	z = x/d
	if z > (1./30.):
		vf = ustar*2.439*log(30*z)
	else:
		vf = 0
	return array([vf,0])

def particula(z,t):
	zp = zeros(4*Nparticulas)
	for i in range(Nparticulas):
		xi = z[4*i:(4*i+2)]
		vi = z[4*i+2:(4*i+4)]
		d = ds[i]
		A = pi*(d/2)**2
		V = (4./3.)*pi*(d/2)**3
		m = rho_particula*V
		W = array([0.,m*g])
		fB = array([0,rho_agua*V*g])
		vf = velocity_field(xi[1],d)
		vrel = vi - vf 
		fD = array([0.75*Cd*norm(vrel)*vrel[0],0.75*Cd*norm(vrel)*vi[1]]) 
		vt = velocity_field(xi[1] + d/2,d)
		vrt = vi - vt
		vb = velocity_field(xi[1] - d/2,d)
		vrb = vi - vb 
		fL = array([0.,0.75*Cl*(norm(vrt[0])**2-norm(vrb[0])**2)], dtype = double) 
		Fi = -W  + alpha*( -fB + fL -  fD)


		if xi[1] <0:
			Fi[1] += -k_penal*xi[1]
		zp[4*i+2:4*i+4] = Fi/m
		for j in range(Nparticulas):
			xj = z[4*j:(4*j+2)]
			vj = z[4*j+2:(4*j+4)]
			dj = ds[j]
			if i>j:
				rij = norm(xi-xj)
				if rij < (d/2 + dj/2):
					tetha = arctan2(((xi[1]-xj[1])**2)**0.5,((xi[1]-xj[0])**2)**0.5)*180/math.pi
					Fi += array([k_penal*(d-rij)*cos(tetha),k_penal*rij*sin(tetha)])
					Fj = -Fi
					zp[4*j+2:4*j+4] += Fj/m
					zp[4*i+2:4*i+4] += Fi/m

		zp[4*i:4*i+2] = vi
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
