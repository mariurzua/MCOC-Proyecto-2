from matplotlib.pylab import *
import time 
Nparticulas = 2

def velocity_field(x):
	z = x[1]/d
	if z > (1./30.):
		vf = ustar*log(30*z)/0.41
		vf = vf * (vf>0)
	else:
		vf = 0
	return array([vf,0])

def fuerzas_hidrodinamicas(x,v,d,area,masa):

	xtop = x + (d/2)*jhat
	xbot = x - (d/2)*jhat
	vf = velocity_field(x + 0*jhat)

	vrelf_top = abs(velocity_field(xtop)[0])
	vrelf_bot = abs(velocity_field(xbot)[0])

	vrel = vf - v
	rho_particula = 2650.
	rho_agua = 1000.
	Cd = 0.47							 #para una particula
	Cl = 0.2
	Cm = 0.5
	g = 9.8
	R = (rho_particula/rho_agua)-1
	alpha = 1/(1 + R + Cm)
	ustar = 0.14  # ustar obtenido de Nino and Garcia (1994)

	fD = (0.5*Cd*alpha*rho_agua*norm(vrel)*area)*vrel

	fL = (0.5*Cl*alpha*rho_agua*(vrelf_top - vrelf_bot)*A)*vrel[0]*jhat

	fW = (-masa*g)*jhat

	Fh = fW + fD + fL

	return Fh

def fondo(x):
	x_mod_d = (x % d) - d/2
	y = sqrt((d/2)**2 - x_mod_d**2)
	return y

def zp_M_particulas(z,t):
	zp = zeros(4*M)

	for i in range(M):
		di = d
		zi = z[4*i:(4*i+4)]
		vi = z[4*i+2:(4*i+4)]

		zp[4*i:(4*i+4)] = zp_una_particula(zi,t)
	zp += zp_choque_M_particulas(z,t,M= M)

	return zp

def zp_choque_M_particulas(z,t,M):
	zp = zeros(4*M)
	for i in range(M):
		xi = z[4*i:(4*i+2)]
		di = d
		area_i, vol_i, masa_i = propiedades_area_volumen_masa(d)
		for j in range(i+1,M):
			xj = z[4*j:(4*j+2)]
			dj = d
			rij = xj - xi
			norm_rij = norm(rij)
			if norm_rij < 0.5*(di+dj):
				area_j,vol_j, masa_j = propiedades_area_volumen_masa(d)
				delta = 0.5*(di+dj)-norm_rij
				nij= rij/norm_rij
				Fj = k_penal*delta*nij
				Fi = -Fj
				zp[4*i+2:(4*i+4)]+=Fi/masa_i
				zp[4*j+2:(4*j+4)]+=Fj/masa_j
	return zp

def propiedades_area_volumen_masa(d):

	rho = 2650
	area = ((d/2)**2)*math.pi
	volumen = (4/3)*(d**3)*math.pi
	masa = rho*volumen

	return area,volumen,masa

def zp_una_particula(z,t):
	zp = zeros(4) 
	xi = z[0:2]
	vi = z[2:4]
	area,vol, masa = propiedades_area_volumen_masa(d)
	F_h = fuerzas_hidrodinamicas(xi,vi,d,area,masa)
	if xi[1] < fondo(xi[0]):
		F_h[1] += -k_penal*xi[1]
	zp[0:2] = vi
	zp[2:4] = F_h/masa

	return zp

ihat = array([1,0])
jhat = array([0,1])

doit = True

start = time.time()

tiempo_bloque_1 = 0
tiempo_bloque_2 = 0
d = 0.15*1e-3

print  "Generating new inital conditions"
itry = 1

x0 = 10*d*rand(Nparticulas)
y0 = 3*d*rand(Nparticulas) + d
while True:
	dmin = infty
	x0 = 30*d*rand(Nparticulas)
	y0 = 3*d*rand(Nparticulas)
	for i in range(Nparticulas):
		xi,yi = x0[i], y0[i]
		for j in range(i+1,Nparticulas):
			xj,yj = x0[j],y0[j]
			dij = sqrt((xi-xj)**2+  (yi-xi)**2)
			dmin = min(dmin,dij)
	print "Try",itry,"dmin/d",dmin/d
	if dmin<1.1*d:
		break
	itry+=1
ustar = 0.14
vx0 = ustar*rand(Nparticulas)
vy0 = 0
rho_agua = 1000./1**3
Cd = 0.47		
A = pi*(d/2)**2
k_penal = 0.5*Cd*rho_agua**norm(vx0)**2/(d/20)

dt = 0.0001 		#paso de tiempo
tmax = 2. 		#tiempo maximo de simulacion
ti = 0.0		#tiempo actual

t = arange(0,tmax,dt)
Nt = len(t)

from scipy.integrate import odeint

z = zeros((Nt,4*Nparticulas))
z[0,0::4] = x0
z[0,1::4] = y0
z[0,2::4] = vx0
z[0,3::4] = vy0

done = zeros(Nparticulas,dtype=int32)
impacting_set = zeros(Nparticulas,dtype=int32)

print "Integrando"

k= 0

if doit:
	while dt*k < int(tmax/dt -1)*dt:
		if k%10 == 0:
			print "k = {} t = {} ".format(k,k*dt)
		zk = z[k,:]
		done *= 0 
		for i in range(Nparticulas):
			irange = slice(4*i,4*i+4)
			zk_i = zk[irange]
			di = d
			if done[i] == 0:
				hay_impacto = False
				impacting_set *= 0  
				M = 1
				for  j in range(i + 1,Nparticulas):
					jrange = slice(4*j, 4*j+4)
					zk_j = zk[jrange]
					dj = d
					rij = zk_j[0:2] - zk_i[0:2]
					if norm(rij) < 0.5*(di+dj)*3:
						hay_impacto= True
						impacting_set[0] = i
						impacting_set[M] = j
						M += 1
				if hay_impacto:
					zk_all = zk_i
					for j in impacting_set[1:M]:
						jrange = slice(4*j , 4*j+4)
						zk_j = zk[jrange]
						zk_all = hstack((zk_all,zk_j))
					ti = time.time()
					zkm1_all = odeint(zp_M_particulas,zk_all, (dt*k,dt*(k+1)))
					tf = time.time()
					tiempo_bloque_1 += tf - ti
					z[k+1,irange]= zkm1_all[1,0:4]
					done[i]=1
					pos_j = 1
					for j in impacting_set[1:M]:
						jrange = slice(4*j,4*j+4)
						z[k+1,jrange] = zkm1_all[1,4*pos_j:4*pos_j+4]
						done[j] = 1
						pos_j += 1

				else:
					ti = time.time()
					zkm1_i = odeint(zp_una_particula,zk_i,(dt*k,dt*(k+1)))
					tf = time.time()
					tiempo_bloque_2  += tf-ti
					z[k+1,irange] = zkm1_i[1,0:4]
					done[i] = 1
		k += 1

figure()
for i in range(Nparticulas):
	plot(z[:,i*4]/d,z[:,i*4+1]/d,'--')
xlabel('Distancia Recorrida: H/d')
ylabel('Altura Recorrida: Z/d')
show()

figure()
subplot(1,2,1)
for i in range(Nparticulas):
	plot(t,z[:,i*4])
xlabel('Tiempo [s]')
ylabel('Distancia Recorrida [m]')
subplot(1,2,2)
for i in range(Nparticulas):
	plot(t,z[:,i*4+1])
xlabel('Tiempo [s]')
ylabel('Altura Recorrida [m]')
show()

figure()
subplot(1,2,1)
for i in range(Nparticulas):
	plot(t,z[:,i*4+2])
xlabel('Tiempo [s]')
ylabel('Velocidad en X [m/s] ')

subplot(1,2,2)
for i in range(Nparticulas):
	plot(t,z[:,i*4+3])
xlabel('Tiempo [s]')
ylabel('Velocidad en Z [m/s] ')

show()
