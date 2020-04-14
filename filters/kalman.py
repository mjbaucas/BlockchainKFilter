from numpy import dot, eye, add, subtract, nan_to_num
from numpy.linalg import inv, pinv
from math import isnan, isinf

def check_val(x):
	if isnan(x):
		return 0.0
	
	if isinf(x):
		if x >= 0:
			return 1.7976931348623157e+308
		else:
			return -1.7976931348623157e+308

	return x

def inv_div(num, den):
	if den == 0:
		if num >= 0:
			return 1.7976931348623157e+308
		else:
			return -1.7976931348623157e+308

	return check_val(num/den)

class KalmanFilter2DPlus(object):
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


class KalmanFilter1D(object):
	def _predict(self, X, U, P, A, B, Q):
		X = check_val(A*X) + check_val(B*U)
		P = check_val(A*P*A) + Q
		return X, P

	def _update(self, X, Z, P, C, R):
		K = inv_div(check_val(P*C),(check_val(C*P*C) + R))
		X = X + check_val(K*(Z - check_val(C*X)))
		P = check_val((1-check_val(K*C))*P*(1-check_val(K*C))) + check_val(K*R*K)
		return X, P

	def filter(self, X, Z, U, P, A, B, C, Q, R):	
		predicted_X, predicted_P = self._predict(X, U, P, A, B, Q)
		new_X, new_P = self._update(predicted_X, Z, predicted_P, C, R)

		return new_X, new_P
