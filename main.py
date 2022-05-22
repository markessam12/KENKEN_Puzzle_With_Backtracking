from kenken import Kenken
import time

t1 = time.time()
# while(True):
game1 = Kenken(7)
game1.solve(forward_check = True, arc_consistency = False)

print((time.time()-t1))
game1.print()
