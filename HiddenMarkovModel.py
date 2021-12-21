# 维特比算法计算过程和大学学的有向图最优路径一样，很容易理解

import numpy as np

class HMM:
    def __init__(self,Ann,Bnm,Pi,O):
        self.A = Ann
        self.B = Bnm
        self.Pi = Pi
        self.O = O
        self.N = np.shape(Ann)[0] #隐马尔科夫模型状态个数
        self.T = np.shape(O)[0]   #观测序列的观测个数，即时刻个数

    def viterbi(self):

        print(self.N,self.T)

        #每个时刻每个状态对应的局部最优状态序列的概率数组
        delta = np.zeros((self.T,self.N))
        #最终shape=(T,N)
        #[[0.10,    0.16,      0.28],   #时刻0每个状态对应的局部最优状态序列的概率
        # [0.028,   0.0504,    0.042],  #时刻1每个状态对应的局部最优状态序列的概率
        # [0.00756, 0.01008,   0.0147]] #时刻2每个状态对应的局部最优状态序列的概率

        # 每个时刻每个状态对应的局部最优状态序列的前导状态索引数组
        psi = np.zeros((self.T,self.N))
        # [[0， 0， 0], #时刻0的前导状态索引
        # [2,  2， 2], #时刻1的前导状态索引
        # [1， 1， 2]] #时刻2的前导状态索引


        for t in range(self.T):
            print("============ init time t = ",t,"=============")
            if 0==t:
                # 计算初值
                print('a_0:', self.Pi.reshape((1, self.N)), '\nb_0:', np.array(self.B[:,O[t]]).reshape((1, self.N)))
                delta[t] = np.multiply(self.Pi.reshape((1,self.N)),np.array(self.B[:,self.O[t]]).reshape((1,self.N)))
                print('delta_t0:', delta[t])
                continue
            for i in range(self.N):
                print('\n...... i = %d'%i)
                print('delta[t%d-1]:'%t, delta[t-1], 'A[:,i%d]'%i, self.A[:,i])
                delta_t_i = np.multiply(delta[t-1],self.A[:,i])

                print('delta_t%d_i%d step1:'%(t,i), delta_t_i)
                delta_t_i = np.multiply(delta_t_i,self.B[i,self.O[t]])
                print('delta_t%d_i%d result:'%(t,i), delta_t_i)

                delta[t,i] = max(delta_t_i)
                psi[t][i] = np.argmax(delta_t_i)

                print('delta:\n', delta)
                print('psi:\n', psi)
            
        states = np.zeros((self.T,))
        t_range = -1 * np.array(sorted(-1*np.arange(self.T)))
        for t in t_range:
            if self.T-1 == t :
                states[t] = np.argmax(delta[t])
            else:
                states[t] = psi[t+1,int(states[t+1])]
        return states



if __name__ == '__main__':

    # 隐马尔可夫模型 λ = (A,B,pi)

    # A转移状态概率分布,状态集合Q的大小N=np.shape(A)[0]
    # 从下给定A可知：Q={盒1, 盒2, 盒3}, N=3
    Ann =np.array([
                [0.5, 0.2, 0.3],
                [0.3, 0.5, 0.2],
                [0.2, 0.3, 0.5]
            ])

    # B观测概率分布，观测集合V的大小T=np.shape(B)[1]
    # 从下面给定的B可知：V={红，白}，T=2
    Bnm = np.array([
            [0.5, 0.5],
            [0.4, 0.6],
            [0.7, 0.3]
        ])
    
    # 初始状态概率分布，初始状态个数=np.shape(pai)[0]
    Pi =  np.array([[0.2],
                    [0.4],
                    [0.4]])

    # 观测序列 ,0表示红色，1表示白，就是(红，白，红)观测序列
    O =  np.array([[0],[1],[0]])

    hmm = HMM(Ann,Bnm,Pi,O)
    states = hmm.viterbi()
    print(states)