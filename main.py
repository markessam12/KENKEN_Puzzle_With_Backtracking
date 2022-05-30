from kenken import Kenken
import matplotlib.pyplot as plt
import time
import math


# Python program to get average of a list
def Average(lst):
    return sum(lst) / len(lst)


t1 = time.time()


# available dimensions
x_axis = [3 ,4,5,6,7 ]
y_axis_forward = []

number_Of_iterations = 10


y_axis_arc = []
y_axis_backtracking = []


avg_time = []
avg_time_value =0

#forward_check
for size in x_axis:
    for k in range(0,number_Of_iterations): #10 times
        game1 = Kenken(size)
        game1.solve(forward_check = True, arc_consistency = False)
        print(size)
        print(k)
        print((time.time()-t1))
        avg_time.append((time.time()-t1))
        game1.print()
        print("#############################################################################################################################################################")

    avg_time_value = Average(avg_time)
    avg_time.clear()
    y_axis_forward.append(avg_time_value)


t1 = time.time()
#arc_consistency
for size in x_axis:
    for k in range(0,number_Of_iterations): #10 times
        game1 = Kenken(size)
        game1.solve(forward_check = True, arc_consistency = True )
        print(size)
        print(k)
        print((time.time()-t1))
        avg_time.append((time.time()-t1))
        game1.print()
        print("#############################################################################################################################################################")

    avg_time_value = Average(avg_time)
    avg_time.clear()
    y_axis_arc.append(avg_time_value)


t1 = time.time()
#Backtracking
for size in x_axis:
    for k in range(0,number_Of_iterations): #10 times
        game1 = Kenken(size)
        game1.solve(forward_check = False, arc_consistency = False )
        print(size)
        print(k)
        print((time.time()-t1))
        avg_time.append((time.time()-t1))
        game1.print()
        print("#############################################################################################################################################################")

    avg_time_value = Average(avg_time)
    avg_time.clear()
    y_axis_backtracking.append(avg_time_value)




plt.ylabel('Average time')
plt.plot(x_axis, y_axis_forward, color='r', label='forward_check')
plt.plot(x_axis, y_axis_arc, color='g', label='arc_consistency')
plt.plot(x_axis, y_axis_backtracking, color='b', label='Backtracking')


new_list = range(math.floor(min(x_axis)), math.ceil(max(x_axis))+1)
plt.xticks(new_list)

plt.legend()
plt.show()
