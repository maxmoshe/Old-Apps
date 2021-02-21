
# coding: utf-8

# In[14]:


import math
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3)

REG_LAMBDA = 0
LEARNING_RATE = 0.1



class Neurale:
    def __init__(self, features, targets, dimensions, activation_function):
        self.activation_function = activation_function #can make this multuiple funcs: self.activation_function[l] = a_f[i]..
        self.features = features
        self.targets = []
        self.example_num = features.shape[0]
        for i in range(self.example_num):
            target = targets[i]
            self.targets.append([0]* len(np.unique(targets))) #unique target values.
            self.targets[i][target] = 1 #Assuming target is 0 or higher, with increment of 1.
            
        
        self.dimensions = dimensions
        self.layer_num = len(dimensions)
        self.weights = []
        self.activations = []
        for l in range(0, self.layer_num-1):
            self.weights.append(np.random.uniform(-1,1, (dimensions[l+1], dimensions[l]+1)))
            self.activations.append(np.zeros(dimensions[l]))
        #self.weights = np.array(self.weights)
        self.activations.append(np.zeros(dimensions[self.layer_num-1]))
                                                       
                                                       
    def forward_prop(self, features):
        self.activations[0] = features
        for l in range(self.layer_num-1): #layers, without output
            for s in range(self.dimensions[l+1]): #sets of weights
                a_sum = 0
                for w in range(len(self.weights[l][s])): #weights
                    if w == 0:
                        a_sum += self.weights[l][s][w] #bias
                    else:
                        a_sum += self.activations[l][w-1] * self.weights[l][s][w]
                self.activations[l+1][s] = self.activation_function(a_sum)

    def backprop(self):
#         deltas = []
#         for l in range(self.layer_num-1): #layers
#             deltas.append([])
#             for s in range(self.dimensions[l+1]): #nodes
#                 deltas[l].append([])
#                 for w in range(len(self.weights[l][s])): #weights
#                     deltas[l][s].append(0)
#                     #deltas[l][n][w] = 0
        deltas = [[np.zeros(self.dimensions[l]+1) for i in range(self.dimensions[l+1])] for l in range(self.layer_num-1)]
        Deltas = [[np.zeros(self.dimensions[l]+1) for i in range(self.dimensions[l+1])] for l in range(self.layer_num-1)]
        
        for i in range(self.example_num):
            error = [np.zeros(self.dimensions[l]) for l in range(self.layer_num)]
            self.forward_prop(self.features[i])
            error[self.layer_num-1] = np.array([self.activations[self.layer_num-1][j] - self.targets[i][j] for j in range(self.dimensions[self.layer_num-1])])
            for l in range(self.layer_num-2, 0, -1):
                nb_weights = self.weights[l][0:,1::] #no bias layer weights.
                error[l] = np.multiply(np.dot(np.transpose(nb_weights),error[l+1]),np.multiply(self.activations[l],1-self.activations[l]))
                #error[l] = np.array(error[l])[1::] remove delta[l][0] for hidden layers. What to for final layer? dimensions incorrect unless i remove delta[l][0]
            for l in range(self.layer_num-1):
                #print(error[l+1], '\n', np.transpose(self.activations[l]))
                #deltas[l] += np.dot(error[l+1],np.transpose(self.activations[l]))
                for i in range(self.dimensions[l+1]):
                    for j in range(self.dimensions[l]+1):
                        if j == 0:
                            deltas[l][i][j] += error[l+1][i]
                        else:
                            deltas[l][i][j] += self.activations[l][j-1]*error[l+1][i]
                
        for l in range(self.layer_num-1): #layers
            for n in range(self.dimensions[l+1]):
                for w in range(self.dimensions[l]+1):
                    if w == 0: #don't reguralize bias weight
                        Deltas[l][n][w] = deltas[l][n][w]/self.example_num
                    else:
                        Deltas[l][n][w] = deltas[l][n][w]/self.example_num + REG_LAMBDA * self.weights[l][n][w] #derivative of j(theta) is equal to the delta.
        return Deltas
    

    def train(self, reps=10000):
        for i in range(reps):
            if i%100==0:
                print(self.cost_function())
            deltas = self.backprop()
            self.gradient_descent(deltas)
    
    def gradient_descent(self, ders):
        for l in range(self.layer_num-1):
            for s in range(self.dimensions[l+1]):
                for w in range(self.dimensions[l]+1):
                    self.weights[l][s][w] -= LEARNING_RATE * ders[l][s][w]

    def check_gradient():
        val = cost_function()
  

    def cost_function(self, weights=None): 
        if weights is None:
            weights = self.weights
        cost = 0
        reg_cost = 0
        right = 0
        for i in range(self.example_num):
            self.forward_prop(self.features[i])
            prediction = self.activations[self.layer_num-1]
            hindex = np.where(prediction == np.amax(prediction))
            prediction = [1 if hindex[0][0] == index else 0 for index in range(len(prediction))]
            if (prediction == self.targets[i]):
                right += 1
#             for k in range(self.dimensions[self.layer_num-1]):
#                 cost -= self.targets[i][k] * math.log(prediction[k]) + (1-self.targets[i][k])*math.log(1-prediction[k])
#             for l in self.weights: #layers
#                 for n in l: #nodes
#                     for w in n: #weights
#                         reg_cost += w**2
#         cost += reg_cost * REG_LAMBDA/(2*self.example_num)
#         cost = cost / self.example_num
        cost = float(right)/self.example_num
        return cost

def logistic_function(x):
    return 1/(1+math.exp(-x)) #exp(x) returns e**x
  

data = np.genfromtxt('iris2.data', delimiter=',')
np.random.shuffle(data)

features = data[0:,:4]
targets = data[0:, 4].astype(int)

netwerk = Neurale(features, targets, [4, 3, 3],logistic_function)


netwerk.train(1000)

for i in range(12): #example prediction/results
    netwerk.forward_prop(netwerk.features[i])
    print(netwerk.activations[netwerk.layer_num-1],netwerk.targets[i])

