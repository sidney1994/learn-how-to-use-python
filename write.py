import random
f = open('test1.txt', 'a')
x=[random.uniform(0,1) for _ in range(11)]
y=[random.uniform(0,1) for _ in range(11)]
z=[random.uniform(0,1) for _ in range(11)]
for i in range(len(x)):
    a1=str(x[i])
    a2=str(y[i])
    a3=str(z[i])
    a4=","
    a5="\n"
    a=a1+a4+a2+a4+a3+a5
    print a
    f.write(a)