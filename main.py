from kenken import Kenken
import time

t1 = time.time()
game1 = Kenken(9)
game1.solve(forward_check = False)

print((time.time()-t1))
print(game1.print())
