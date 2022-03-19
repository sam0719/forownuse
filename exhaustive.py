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

content = MIMEMultipart()  #建立MIMEMultipart物件

content["from"] = "sam07190719@gmail.com"  #寄件者
content["to"] = "sam07190719@gmail.com" #收件者

sender = 'sam07190719@gmail.com'
password='quaggqvwudewcyzj'


np.set_printoptions(formatter={'float': '{: 0.6f}'.format})

# gate=int(input("gate數:"))
gate=7
seven_gate_begin,seven_gate_end=input("深度7範圍:(空格分割,例如:如果只要跑1單個區間,就輸入1 1)").split(" ")
range_begin,range_end=input("深度6範圍:(空格分割,例如:如果只要跑1單個區間,就輸入1 1)").split(" ")
range_begin=int(range_begin)
range_end=int(range_end)
seven_gate_begin=int(seven_gate_begin)
seven_gate_end=int(seven_gate_end)

# 遞迴
bit=3
# test_target=np.array([[7.0710671e-01+0.j,4.9999994e-01+0.49999994j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j],
#  [7.0710671e-01+0.j,-4.9999994e-01-0.49999994j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j],
#  [0.0000000e+00+0.j,0.0000000e+00+0.j,-4.9999988e-01-0.49999988j,5.1132716e-09,-0.7071066j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j],
#  [0.0000000e+00+0.j,0.0000000e+00+0.j,-4.9999988e-01-0.49999988j,-5.1132716e-09+0.7071066j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j],
#  [0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,5.1132716e-09,-0.7071066j,4.9999985e-01-0.49999985j,0.0000000e+00+0.j,0.0000000e+00+0.j],
#  [0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,5.1132716e-09,-0.7071066j,-4.9999985e-01+0.49999985j,0.0000000e+00+0.j,0.0000000e+00+0.j].
#  [0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,-4.9999976e-01+0.49999976j,-7.0710641e-01+0.j].
#  [0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,0.0000000e+00+0.j,-4.9999976e-01+0.49999976j,7.0710641e-01+0.j]])
#H = np.matrix("1 1; 1 -1") / np.sqrt(2)
#I = np.matrix("1 0; 0 1")
#T = np.matrix(f"1 0; 0 {math.cos(math.pi/4)+0.7071067811865476j}")
#U = np.matrix(f"1 0; 0 {math.cos(math.pi/4)-0.7071067811865476j}")
#Cnot=np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0")
#Cnot_T=np.matrix("1 0 0 0; 0 0 0 1; 0 0 1 0; 0 1 0 0")
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
#target=np.matrix("1 0 0 0 0 0 0 0; 0 1 0 0 0 0 0 0; 0 0 1 0 0 0 0 0; 0 0 0 1 0 0 0 0; 0 0 0 0 1 0 0 0; 0 0 0 0 0 1 0 0; 0 0 0 0 0 0 0 1; 0 0 0 0 0 0 1 0")
#array_dict={1:['H','0','0'],2:['0','H','0'],3:['0','0','H'],4:['T','0','0'],5:['0','T','0'],6:['0','0','T'],7:['U','0','0'],8:['0','U','0'],9:['0','0','U'],10:['1','2','0'],11:['0','1','2'],12:['1','0','2'],13:['0','0','0']}
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
    #"BC":np.matrix("1 0 0 0 0 0 0 0; 0 1 0 0 0 0 0 0; 0 0 1 0 0 0 0 0; 0 0 0 1 0 0 0 0; 0 0 0 0 0 1 0 0; 0 0 0 0 1 0 0 0; 0 0 0 0 0 0 0 1; 0 0 0 0 0 0 1 0"),
    #"BC_T":np.matrix("1 0 0 0 0 0 0 0; 0 0 0 0 0 1 0 0; 0 0 1 0 0 0 0 0; 0 0 0 0 0 0 0 1; 0 0 0 0 1 0 0 0; 0 1 0 0 0 0 0 0; 0 0 0 0 0 0 1 0; 0 0 0 1 0 0 0 0")
    }
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
# a=np.array([matrix[1],matrix[2]])
# print(a.shape)
# print(np.einsum('ij,ji->i',a.T.dot(a),a).shape)
# for i in a:
#     ans=np.matmul(i,a) # 
#     for j in a:
#         ans=np.matmul(j,ans)
#         ans=np.matmul(I8,ans)
#         print(np.transpose(np.conj(ans)).shape)
#         num = np.abs( np.trace( mat ) )
#         dem = 3
#         ans=(1 - ( num / dem )  )
#         print(ans)
        
        
#target=np.matrix("1 0 0 0 0 0 0 0; 0 1 0 0 0 0 0 0; 0 0 1 0 0 0 0 0; 0 0 0 1 0 0 0 0; 0 0 0 0 1 0 0 0; 0 0 0 0 0 1 0 0; 0 0 0 0 0 0 0 1; 0 0 0 0 0 0 1 0")
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
I8=np.kron(np.kron(I,I),I)

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

                

def F2(matrix): #矩陣互相乘以後存起來再乘自己
    ans={}
    key=matrix.keys()
    value=matrix.values()
    for i in range(len(matrix)):
        print(i)
        for j in range(len(matrix)):
            ans[f"{i}-{j}"]=(list(value)[j] @ list(value)[i]).astype(np.csingle)
    return ans
# a1=F2(matrix)  
# print(len(a1))
# a2=F2(a1)
# print(len(a2))

def F3(M1,M2,M3):
    global gbest_fitness,gbest
    ans=np.dot(matrix[M2],matrix[M1])
    ans=np.dot(matrix[M3],ans)
    ans=np.dot(ans,I8)
    fitness=cal_fitness(ans,target)
    if fitness<gbest_fitness:
        gbest_fitness=fitness
        gbest=(M1,M2,M3)
        print(gbest_fitness,gbest)


# function=np.vectorize(F4)
# param=[x for x in range(1,82,1)]
# function(param,param2,param3,param4)
    
# loop_val=[]
# for i in range(3):
#     loop_val.append([x for x in matrix.keys()])
# print(loop_val)
# if __name__ == '__main__':
#     pool = multiprocessing.Pool()                    
#     p=multiprocessing.Pool(3)
#     loop_val = np.array([x for x in matrix.values()])
#     x1,x2,x3=np.split(loop_val,[25,50])
# #     print(x1,x2,x3)
# #     print(loop_val)
#     print("!")
#     b = p.map(Fmatrix.F2, x1)
#     print(b)
#     b = p.map(Fmatrix.F2, x2)
#     print(b)
#     b = p.map(Fmatrix.F2, x3)
#     print(b)
    
    
# cProfile.run('F(gate)')
# cProfile.run('R(gate)')

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
M2=R3(matrix)
# print(list(M2.keys())[2095])
# print(count_matrix[43])
# print(count_matrix[38])
# print(count_matrix[49])
# print(count_matrix[49])

# print((np.abs(matrix[49]@matrix[49]@test_target-matrix[43]@matrix[49]@I8)<0.01).all())

content["subject"] = f"結果:總深度:7,深度7範圍:{seven_gate_begin}~{seven_gate_end},深度6範圍:{range_begin,range_end}"  #郵件標題

values=list(matrix.values())
keys=list(matrix.keys())
matrix_len=len(matrix)
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

print(len(matrix))
for i in range(seven_gate_begin,seven_gate_end+1):
    print("深度7:",i)
    ans=matrix[i]@target
    for j in range(range_begin,range_end+1):
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
###########4-4#################
                        content.attach(MIMEText("\r\n"))#換行:\r\n
content.attach(MIMEText("----------------------------\r\n"))
content.attach(MIMEText("如果上面沒有內容就是沒有解"))
with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
    try:
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.starttls()  # 建立加密傳輸
        smtp.login(sender, password)  # 登入寄件者gmail
        smtp.send_message(content)  # 寄送郵件
        print("Complete!")
    except Exception as e:
        print("Error message: ", e)
# with open('file.txt', 'w') as file:
#      file.write(json.dumps(M2)) 
# M4=R2(M2)
# print(len(M4))

# F(gate)
# 遞迴       
# R(deep=gate) 


# a=[np.zeros((8,8)) for x in range(87*87)]
# b=[np.random.rand(8,8) for x in range(87*87-1)]
# b.append(np.zeros((8,8)))
# for i in range(len(b)):
#     print(i)
#     for j in range(len(a)):
#         if (np.abs(b[i]-a[j])<0.01).all():
#             print(i,j,"find!")

# I8=np.kron(np.kron(I,I),I)
# a1=np.dot(matrix[41],I8)
# a2=np.dot(matrix[35],a1)
# a3=np.dot(matrix[78],a2)
# a4=np.dot(matrix[53],a3)
# a5=np.dot(matrix[77],a4)
# a6=np.dot(matrix[31],a5)
# print(cal_fitness(a6,target))

output_file = "exhaustive_"+str(6)+".csv"

# for i in range(0,40,1):
#     print(i)

#for回圈
# for k4 in range(0,40,1):
#     ans=np.kron(np.kron(I,I),I)
#     ans=np.dot(matrix[k4+1],ans)
#     for k3 in range(len(matrix)):
#         ans2=np.dot(matrix[k3+1],ans)
#         for k2 in range(len(matrix)):
#             ans3=np.dot(matrix[k2+1],ans2)
#             for k in range(len(matrix)):
#                 ans4=np.dot(matrix[k+1],ans3)
#                 for j in range(len(matrix)):
#                     ans5=np.dot(matrix[j+1],ans4)
#                     for i in range(len(matrix)):
#                         ans6=np.dot(matrix[i+1],ans5)
#                         result=cal_fitness(ans6,target)
#                         if result < gbest_fitness:
#                             gbest_fitness=result
#                             gbest=[f"{k4}-{k3}-{k2}-{k}-{j}-{i}",ans]
#                             print(result,f"{k4}-{k3}-{k2}-{k}-{j}-{i}")
#                             with open(output_file, 'a', newline='') as csvfile:
#                                 writer = csv.writer(csvfile)
#                                 writer.writerow([result,f"{k4}-{k3}-{k2}-{k}-{j}-{i}"])




endtime = datetime.datetime.now()

print ((endtime - starttime).seconds)
os.system("pause")
