from matplotlib.pylab import *


#-------- Hecho en clases ----------------

#Unidades bases SI
_m = 1. 
_kg = 1.
_s = 1.
_mm = 1e-3*_m
_gr = 1e-3*_kg



vfx = 5.0 # m/s
vfy = 0.0 # m/s

x0 = array([0., 1.], dtype=double)
v0 = array([1., 1.], dtype=double)

xi =x0 # posicion actual
vi = v0 # velocidad actual 
xim1 = zeros(2, dtype=double) # posicion siguiente 
vim1 = zeros(2, dtype=double) # velocidad siguiente

g = 9.81*_m/_s**2
d= 1*mm
rho = 2700.*_kg/(_m**3)
m = rho*(4./3./8)*pi*(d**3)
Cd = 0.47
#Inicializar Euler en x0 


dt = 2e-6*_s #paso de tiempo
tmax = 1.*_s #tiempo maximo de simulacion
ti = 0.*_s #tiempo actual

W = array([0., -m*g])
vf = array([vfx,vfy])

Nt = int32(2*tmax/dt)
x_store = zeros((2,Nt))
v_store = zeros((2,Nt))
t_store = zeros(Nt)



i = 0
#Metodo de Euler 
while ti < tmax:
	print "ti = ", ti
	print "xi = ", xi
	print "vi = ", vi

	#evaluar v. relativa
	vrel = vf - vi
	norm_vrel = vrel.norm()
	#evaluar fuerzas sobre la particula
	fD = 0.5*Cd*norm_vrel*vrel
	Fi = W + fD
	#evaluar aceleracion
	ai = Fi/m
	#integrar	
	xim1 = xi + vi*dt + ai*(dt**2/2)
	vim1 = vi + ai*dt
	#avanzar al siguiente paso
	x_store[:,i] = xi  
	v_store[:,i] = vi 
	t_store[i] = ti
	ti += dt
	xi = xim1
	vi = vim1
	i+=1

#guardar el ultimo paso
x_store[:,i] = xi  
v_store[:,i] = vi 
t_store[i] = ti

figure()

#-------- END ----------------------------

#Logarithmic velocity profile (rough wall)
#def Logarithmic_velocity_profile_rough_wall(z): # z is the wall-normal coordinate
#	k = 0.41 # von Karmán constant 
#	uf = (1.0/k)*np.ln(30.0*z) #Fluid velocity in the stream-wise direction
#	return uf
#
# Equations of all Hydrodynamics Forces 
#def Submerged_gravity_force(rhos,rho,g,dp,us):
#	R = (rhos/rho) - 1
#	Fsg =  (R*dp*g)/(us**2)
#	return Fsg
#
#def Non-linear_drag_force(cd,up,uf):
#	Fd = (3/4)*cd*(up-uf)*((up**2-uf**2)**0.5)
#	return = Fd
#
#def Basset_force(rhos,rho,g,dp,nu,uf,up):
#
#def Virtual_mass_force(cm,uf,dt):
#	Fvm = cm*uf*dt 
#	return Fvm
#
#def Magnus_force():
#
#def Lift_force(cl,urt,urb,e):
#	Fl = (3/4)*cl*(urt**2-urb**2)*e
#	return Fl
#
# Function of Shear Velocity
#def Shear_velocity(tau,rhos,rho,g,dp):
#	R = (rhos/rho) - 1
#	us = (tau*R*g*dp)**0.5
#	return us
#
# Properties of the particle 
#dp = 0.001   # m - Diameter of a particle of sand 0,0625-2 mm
#area = ((d/2)**2)*np.pi() # m^2 - Area of a particle of sand 
#volume = (4/3)*np.pi()*(d/2)**3 # m^3 - Area of a particle of sand
#rhos = 1570. # Kg/m^3 - Density of sand 1550 to 1600 Kg/m3
#
# Properties water
#rho = 998. # Kg/m^3 - Density of water 
#
#General properties
#g = 9.8 # m/s^2
#
#
#Initial Conditions
#dt = 1. # s
#T = 100000 # s
#x = 
#
#for  i in range(100000):
#	t = i*dt
#	x[i+1]= x[i] +  u[i]*dt + (a[i]*(dt^2))/2
#
#
#
#---------

