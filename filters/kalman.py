from numpy import dot, eye, add, subtract, nan_to_num
from numpy.linalg import inv, pinv

class KalmanFilter(object):
	def _predict(self, X, U, P, A, B, Q):
		X = nan_to_num(dot(A, X)) + nan_to_num(dot(B, U))
		P = nan_to_num(dot(A, nan_to_num(dot(P, A.T)))) + Q 		
		return X, P

	def _update(self, X, Z, P, C, R):		
		n = len(X)
		K = nan_to_num(dot(P, nan_to_num(dot(C.T, pinv(nan_to_num(dot(C, nan_to_num(dot(P, C.T)))) + R)))))
		X = X + nan_to_num(dot(K, Z - nan_to_num(dot(C, X))))
		P = nan_to_num(dot(eye(n) - nan_to_num(dot(K,C)), nan_to_num(dot(P, (eye(n) - nan_to_num(dot(K,C))).T)))) + nan_to_num(dot(K, nan_to_num(dot(R, K.T))))   
		return X, P		  
	 	
	def filter(self, X, Z, U, P, A, B, C, Q, R):	
		predicted_X, predicted_P = self._predict(X, U, P, A, B, Q)
		new_X, new_P = self._update(predicted_X, Z, predicted_P, C, R)
		return new_X, new_P


