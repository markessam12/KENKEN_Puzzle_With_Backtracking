from kenken import Kenken
import matplotlib.pyplot as plt
import time
import math
import sys

def progress(j):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
    sys.stdout.flush()

# available dimensions
x_axis = [3 , 4, 5, 6, 7]

number_Of_iterations = 10

y_axis_arc = []
y_axis_backtracking = []
y_axis_forward = []

avg_time = []
avg_timeBC = 0
avg_timeFC = 0
avg_timeAC = 0
i = 0
n = 3 * number_Of_iterations * len(x_axis)

#forward_check
for size in x_axis:
    for k in range(0, number_Of_iterations):
        game1 = Kenken(size)
        t1 = time.time()
        game1.solve(forward_check = False, arc_consistency = False)
        avg_timeBC += (time.time()-t1)
        i += 1
        progress(i / n)

        t1 = time.time()
        game1.solve(forward_check=True, arc_consistency=False)
        avg_timeFC += (time.time()-t1)
        i += 1
        progress(i / n)

        t1 = time.time()
        game1.solve(forward_check=True, arc_consistency=True)
        avg_timeAC += (time.time()-t1)
        i += 1
        progress(i/n)

    y_axis_backtracking.append(avg_timeBC/number_Of_iterations)
    y_axis_forward.append(avg_timeFC/number_Of_iterations)
    y_axis_arc.append(avg_timeAC/number_Of_iterations)
    avg_timeBC = 0
    avg_timeFC = 0
    avg_timeAC = 0

plt.ylabel('Average time')
plt.plot(x_axis, y_axis_forward, color='r', label='forward_check')
plt.plot(x_axis, y_axis_arc, color='g', label='arc_consistency')
plt.plot(x_axis, y_axis_backtracking, color='b', label='Backtracking')


new_list = range(math.floor(min(x_axis)), math.ceil(max(x_axis))+1)
plt.xticks(new_list)

plt.legend()
plt.show()
