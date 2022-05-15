from kenken import Kenken
import time

t1 = time.time_ns()
for i in range(100):
    game1 = Kenken(3)
    game1.solve()

print((time.time_ns()-t1))
print(game1.print())
