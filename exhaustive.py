import os
os.environ['NUMPY_EXPERIMENTAL_ARRAY_FUNCTION'] = '0'
import numpy as np
#import cupy as np
import datetime
import csv
np.set_printoptions(linewidth=100)

import math
import cmath
import multiprocessing
from itertools import product
import cProfile
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys


content = MIMEMultipart()  #建立MIMEMultipart物件

content["from"] = "sam07190719@gmail.com"  #寄件者
content["to"] = "sam07190719@gmail.com" #收件者

sender = 'sam07190719@gmail.com'
password='quaggqvwudewcyzj'


np.set_printoptions(formatter={'float': '{: 0.6f}'.format})

# gate=int(input("gate數:"))
gate=7

# 遞迴
bit=3

i = complex(0, 1)
I = np.array( [[1, 0],
               [0, 1]],dtype=np.csingle)
H = 1/(cmath.sqrt(2)) * np.array([[1, 1], 
                                  [1, -1]],dtype=np.csingle)
T  = np.array( [[1, 0], 
                [0, cmath.exp(i*cmath.pi/4)]],dtype=np.csingle)
U = np.array( [[1, 0], 
                [0, cmath.exp(-i*cmath.pi/4)]],dtype=np.csingle)

Cnot = np.array( [[1, 0, 0, 0], 
                  [0, 1, 0, 0], 
                  [0, 0, 0, 1], 
                  [0, 0, 1, 0]],dtype=np.csingle)

Cnot_T = np.array( [[1, 0, 0, 0], 
                    [0, 0, 0, 1], 
                    [0, 0, 1, 0], 
                    [0, 1, 0, 0]],dtype=np.csingle)

target = np.array ([[1, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 1, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0]],dtype=np.csingle)
num_to_matrix_dict={
    "H":H,
    "T":T,
    "U":U,
    "C":Cnot,
    "C_T":Cnot_T,
    "I":I,
    
    "BC": np.array( [[1,0,0,0,0,0,0,0],
                      [0,1,0,0,0,0,0,0],
                      [0,0,1,0,0,0,0,0],
                      [0,0,0,1,0,0,0,0],
                      [0,0,0,0,0,1,0,0],
                      [0,0,0,0,1,0,0,0],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,1,0]] ,dtype=np.csingle),
    "BC_T": np.array( [[1,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,0,0],
                       [0,0,1,0,0,0,0,0],
                       [0,0,0,0,0,0,0,1],
                       [0,0,0,0,1,0,0,0],
                       [0,1,0,0,0,0,0,0],
                       [0,0,0,0,0,0,1,0],
                       [0,0,0,1,0,0,0,0]] ,dtype=np.csingle)
}
I8=np.kron(np.kron(I,I),I)
def cal_fitness(X,Y):
    if (np.abs(X-Y)<0.01).all():
        return 0
    else:
        return 1
#   ans=[]
#   mat = np.matmul( np.transpose( np.conj( X ) ), Y )
#   num = np.abs( np.einsum("ii",mat) )
#   dem = mat.shape[0]
#   ans=(1 - ( num / dem )  )
#   return ans 




starttime = datetime.datetime.now()

matrix={}
count_matrix={}
#先把每個矩陣的字典計算出來
count=1
for i in ["H","T","U","I","C","C_T","BC","BC_T"]:
    a=num_to_matrix_dict[i]
    for j in ["H","T","U","I","C","C_T"]:
        if i=="BC" or i=="BC_T":
            count_matrix[count]=f"{i}"
            matrix[count]=a
            count+=1
            break
        else:
            if (i=="C_T"or i=="C") and (j=="C" or j=="C_T"):
                continue
            b=np.kron(a,num_to_matrix_dict[j])
        for k in ["H","T","U","I"]:
            if j == 'C' or j == "C_T":
                count_matrix[count]=f"{i}{j}"
                matrix[count]=b
                count+=1
                break
            elif i=="C" or i=="C_T":
                count_matrix[count]=f"{i}{j}"
                matrix[count]=b
                count+=1
                break
            elif i=="I" and j=="I" and k=="I":
                continue
            else:
                c=np.kron(b,num_to_matrix_dict[k])
            count_matrix[count]=f"{i}{j}{k}"
            matrix[count]=c
            count+=1
g=2
value=list(matrix.values())
        
gbest_fitness=2
gbest=[]
# gate = 3
output_file = "exhaustive_"+str(gate)+".csv"
def R(deep=3,Rmatrix=np.kron(np.kron(I,I),I),index=[]):
    global gate
    global gbest_fitness,gbest
    if deep==0:
        return cal_fitness(Rmatrix,test_target)
    if deep==gate:
        range_length=range(range_begin,range_end+1,1)
    else:
        range_length=range(len(matrix))
    for j in range_length:
        if deep==gate:
            print("第一個gate:",j+1)
            print("第二個gate:")
            with open(f"exhaustive_{str(gate)}_log_{range_begin+1}to{range_end+1}.csv", 'a') as file:
                file.write(f"第一個gate:{j+1}")
                
        elif deep+1==gate:
            print(j+1)
            with open(f"exhaustive_{str(gate)}_log_{range_begin+1}to{range_end+1}.csv", 'a',newline='') as csvfile:
                csvfile.write("第二個gate:")
                writer = csv.writer(csvfile)
                writer.writerow([j+1,Rmatrix])
        
        fitness=R(deep-1,np.dot(matrix[j+1],Rmatrix),index+[j+1])
        if len(index+[j+1])==gate:
            if fitness==0:
                gbest_fitness=fitness
                gbest=index+[j+1]
                print(fitness,gbest)
                with open(output_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([fitness,gbest])     


def F(deep=3):
    flag=0
    flag2=0
    global gbest_fitness,gbest
    loop_val=[]
    for i in range(deep):
        if i ==0:
            loop_val.append([list(matrix.keys())[x] for x in range(range_begin,range_end+1,1)])
        else:
            loop_val.append([x for x in matrix.keys()])
    for i in  product(*loop_val):
        if i[0]!=flag2:
            print("第一個gate:",i[0])
            print("第二個gate:")
            flag2=i[0]
        if i[1]!=flag:
            print(i[1])
            flag=i[1]
        Rmatrix=I8
        for j in i:
            Rmatrix=np.dot(matrix[j],Rmatrix)
        fitness=cal_fitness(Rmatrix,target)
        if fitness==0:
            gbest_fitness=fitness
            gbest=i
            print(gbest_fitness,gbest)
            with open(output_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([gbest_fitness,gbest])



def R2(M):
    dict={}
    key=list(M.keys())
    value=list(M.values())
    for i in range(len(M)):
        for j in range(len(M)):
            for k in range(len(M)):
                dict[f"{key[i]}-{key[j]}-{key[k]}"]=value[k]@value[j]@value[i]
    return dict  

def R3(M):
    dict={}
    key=list(M.keys())
    value=list(M.values())
    for i in M:
        for j in M:
            for k in M:
                dict[f"{i}-{j}-{k}"]=(M[k]@(M[j]@M[i]))
    return dict
def R4(M):
    dict={}
    key=list(M.keys())
    value=list(M.values())
    for i in M:
        for j in M:
            for k in M:
                for l in M:
                    dict[f"{i}-{j}-{k}-{l}"]=(M[l]@(M[k]@(M[j]@M[i])))
                
    return dict 

# for i in range(1):
#     print(i)
#     ans=values[i]@target
#     for j in range(1):
#         print(j)
#         ans2=values[j]@ans
#         for j2 in range(matrix_len):
#             print(j2)
#             ans3=values[j2]@ans2
#             for k in range(len(M2values)):
#                 if(np.abs(ans3-M2values[k])<0.01).all():
#                     print(j2,k,"find")
###########3-3###############
if __name__ == '__main__':
    try:
        seven_gate_begin,seven_gate_end,range_begin,range_end=sys.argv[1:5]
    except Exception as e:
        print(sys.argv)
        print(e)
    seven_gate_begin=int(seven_gate_begin)
    seven_gate_end=int(seven_gate_end)
    range_begin=int(range_begin)
    range_end=int(range_end)
    print(f"深度7範圍:{seven_gate_begin}~{seven_gate_end},深度6範圍:{range_begin}~{range_end}")
#     seven_gate_begin,seven_gate_end=input("深度7範圍:(空格分割,例如:如果只要跑1單個區間,就輸入1 1)").split(" ")
#     range_begin,range_end=input("深度6範圍:(空格分割,例如:如果只要跑1單個區間,就輸入1 1)").split(" ")
#     range_begin=int(range_begin)
#     range_end=int(range_end)
#     seven_gate_begin=int(seven_gate_begin)
#     seven_gate_end=int(seven_gate_end)

    M2=R3(matrix)

    content["subject"] = f"結果:總深度:7,深度7範圍:{seven_gate_begin}~{seven_gate_end},深度6範圍:{range_begin,range_end}"  #郵件標題

    values=list(matrix.values())
    keys=list(matrix.keys())
    matrix_len=len(matrix)
    print(len(matrix))
    for i in range(seven_gate_begin,seven_gate_end+1):
        print("深度7:",i)
        ans=matrix[i]@target
        for j in range(range_begin,range_end+1):
            content = MIMEMultipart()  #建立MIMEMultipart物件
            content["from"] = "sam07190719@gmail.com"  #寄件者
            content["to"] = "sam07190719@gmail.com" #收件者
            content["subject"] = f"結果:總深度:7,深度7:{i},深度6:{j}"  #郵件標題
            print("深度6:",j)
            ans2=matrix[j]@ans
            for j2 in matrix:
                ans3=matrix[j2]@ans2
                for j3 in matrix:
                    ans4=matrix[j3]@ans3
                    for k in M2:
                        if(np.abs(ans4-M2[k])<0.01).all():
                            print(k,j3,j2,j,i,"find")
                            content.attach(MIMEText(f"{k}-{count_matrix[j3]}-{count_matrix[j2]}-{count_matrix[j]}-{count_matrix[i]}\r\n"))  #郵件內容
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                try:
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    smtp.login(sender, password)  # 登入寄件者gmail
                    smtp.send_message(content)  # 寄送郵件
                except Exception as e:
                    print("Error message: ", e)
                                ###########4-4#################
                    content.attach(MIMEText("\r\n"))#換行:\r\n


    output_file = "exhaustive_"+str(6)+".csv"






    endtime = datetime.datetime.now()

    print ((endtime - starttime).seconds)
    os.system("pause")
