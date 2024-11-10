import pandas as pd
import numpy as np
import copy, math

class modelML:
    def __init__(self, X, Y):
        self.X_train = X
        self.Y_train = Y
        self.w = np.zeros(X.shape[1])
        self.b = 0

    def compute_cost(self, X, Y, w, b):
        m = X.shape[0]
        cost = 0.0
        for i in range(m):
            f_wb_i = np.dot(X[i], w) + b
            cost = cost + (f_wb_i - Y[i])**2
        cost = cost / (2 * m)

        return cost
    
    def compute_gradient(self, X, Y, w, b):
        m, n = X.shape
        dj_dw = np.zeros((n,))
        dj_db = 0.0

        for i in range(m):
            err = (np.dot(X[i], w) + b) - Y[i]
            for j in range(n):
                dj_dw[j] += err * X[i, j]
            dj_db += err
        dj_dw = dj_dw / m
        dj_db = dj_db / m
        
        return dj_db, dj_dw
    
    def gradient_descent(self, X, y, w_in, b_in, alpha, num_iters): 
        J_history = []
        w = copy.deepcopy(w_in)
        b = b_in
        
        for i in range(num_iters):
            dj_db, dj_dw = self.compute_gradient(X, y, w, b)

            # Cập nhật tham số w, b
            w = w - alpha * dj_dw
            b = b - alpha * dj_db

            # Lưu chi phí tại mỗi lần lặp
            if i < 100000:
                J_history.append(self.compute_cost(X, y, w, b))

            # In chi phí sau mỗi khoảng nhất định
            if i % math.ceil(num_iters / 10) == 0:
                print(f"Iteration {i:4d}: Cost {J_history[-1]:8.2f}")
            
        return w, b, J_history
    
X_train = np.array([[1, 2], [3, 4], [5, 6]])  # Ví dụ giả sử bạn có 100 mẫu và 3 đặc trưng
y_train = np.array([2, 4, 6])     # Ví dụ giả sử mục tiêu có 100 giá trị

modelML = modelML(X_train, y_train)
w_init = np.zeros(X_train.shape[1])
b_init = 0
alpha = 0.01
iterations = 1000

w_final, b_final, J_history = modelML.gradient_descent(X_train, y_train, w_init, b_init, alpha, iterations)
print(w_final)
print(b_final)