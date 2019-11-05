from matplolib.pylab import *

reuse_initial_condition = False

doit = True

start = Time.time()

tiempo_bloque_1 = 0
tiempo_bloque_2 = 0

if reuse_initial_condition:
	print "Reusing initial conditions"
	data = load("Initial_condition.npz")
	x0 = data["x0"]
	y0 = data["y0"]
	vx0 = data["vx0"]
	vy0 = data["vy0"]
	Nparticulas = data["Nparticulas"]
else:
	print  "Generating new inital conditions"
	itry = 1
	while True:
		dmin = infty
		x0 = 10*d*rand(Nparticulas)
		y0 = 3*d*rand(Nparticulas)
		for i in range(Nparticulas):
			xi,yi = x0[i], y0[i]
			for j in range(Nparticulas):
				xj,yj = x0[j],y0[j]
				dij = sqrt((xi-xj)**2-(yi-xi)**2)
				dmin = min(dmin,dij)
		print "Try",itry,"dmin/d",dmin/d
		if dmin<1.1*d:
			break
		itry+=1
	vx0 = ustar*rand(Nparticulas)
	vy0 = 0
	save=("initial_condition.npz",x0=x0,y0=y0,vx0=vx0,vy0=vy0,Nparticulas=Nparticulas)

t = arange(0,tmax,dt)
Nt = len(t)

from scipy.integrate import odeint

z = zeros((Nt,4*Nparticulas))
z[0,0:4] = x0
z[0,1:4] = y0
z[0,2:4] = vx0
z[0,3:4] = vy0

done =zeros(Nparticulas,dtype=int32)
impacting_set = zeros(Nparticulas,dtype=int32)

print "Integrando"

k= 0

if doit:
	while dt*k < int(tmax/dt -1)*dt:
		if k%10 == 0:
			print "k = {} t = {} ",format(k,k*dt)
		zk = z[k,:]
		done *= 0 #nose si es *= o =
		for i in range(Nparticulas):
			irange = slice(4*i,4*i+4)
			zk_i = zk[irange]
			di = d
			if done[i] == 0:
				hay_impacto = False
				impacting_set *= 0 #nose si es *= o =  
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
						M+=1
				if hay_impacto:
					zk_all = zk_i
					for j in impacting_set[1:M]:
						jrange = slice(4*j , 4*j+4)
						zk_j = zk[jrange]
						zk_all = hstack((zk_all,zk_j))
					ti = time.time()

					zkm1_all = odeint (zp_M_particulas,zk_all, (dt*k,dt*(k+1)))


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
else:
	data = load("solution.npz")
	t = data["t"]
	z = data["z"]
	dt = data["dt"]


def zp_M_particulas(z,t,M):
	zp = zeros(4*M)

	for i in range(M):
		di = d
		zi = z[4*i:(4*i+4)]
		vi = z[4*i+2:(4*i+4)]

		zp[4*i:(4*i+4)] = zp_una_particula(zi,t,di)
	zp += zp_choque_M_particulas(z,t,M= M)

	return zp

def zp_choque_M_particulas(z,t,M):
	zp = zeros(4*M)
	for i in range(M):
		xi = z[4*i:(4*i+2)]
		di = d
		area_i, vol_i, masa_i = propiedades_area_volumen_masa()
		for j in range(i+1,M):
			xj = z[4*j:(4*j+2)]
			dj = d
			rij = xj - xi
			norm_rij = norm(rij)
			if norm_rij < 0.5*(di+dj):
				area_j,vol_j, masa_j = propiedades_area_volumen_masa()
				delta = 0.5*(di+dj)-norm_rij
				nij= rij/norm_rij
				Fj = k_penal*delta*nij
				Fi = -Fj
				zp[4*i+2:(4*i+4)]+=Fi/masa_i
				zp[4*j+2:(4*j+4)]+=Fj/masa_j
	return zp
				