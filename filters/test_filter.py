from numpy import array, eye, diag, zeros, arange, ndarray, dot, empty, append, nan_to_num
from numpy.linalg import norm
from numpy.random import multivariate_normal, randn
import matplotlib.pyplot as plt

from kalman import KalmanFilter

if __name__ == "__main__":
	T = 1e-3
	t = list(arange(0, 1, T))
	n = 3
	m = 3
	A = array([[1, T, 0], [0, 1, T], [-557.02, -28.616, 0.9418]])
	B = array([0, 0, 557.02]).T
	C = eye(n)
	Q = diag([1e-5, 1e-3, 1e-1])
	R = diag([1e-4, 1e-2, 1])
	
	W = zeros((len(t), n))
	for i in range(len(t)):
		W[i, :] = multivariate_normal(W[i, :], Q)
	W = W.T	

	V = zeros((len(t), m))
	for i in range(len(t)):
		V[i, :] = multivariate_normal(V[i, :], R)	
	V = V.T		

	X = zeros((n, len(t)))
	Z = zeros((m, len(t)))
	U = randn(1, len(t))[0,:]
	U = U / max(abs(U))
	for i in range(len(U)):
		if i >= len(t)/2:
			U[i]+=1

	P_KF = zeros((n,n,len(t)))
	X_KF = X
	P_KF[:,:,0] = 10*Q
	A_KF = A
	
	kf = KalmanFilter()
	for k in range(1, len(t)-1):
		X[:, k+1] = nan_to_num(dot(A, X[:, k])) + nan_to_num(dot(B, U[k])) + W[:, k]
		Z[:, k+1] = nan_to_num(dot(C, X[:, k+1])) + V[:, k+1]
		
		X_KF[:, k+1], P_KF[:, :, k+1] = kf.filter(X_KF[:, k], Z[:, k+1], U[k], P_KF[:, :, k], A_KF, B, C, Q, R)

	plt.plot(t, X[0,:])
	plt.plot(t, X_KF[0,:])
	plt.savefig('test2.png')
