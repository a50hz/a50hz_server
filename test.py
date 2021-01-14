import numpy as np
a = np.arange(1.01, 1.51, 0.01)
for k in a:
    print(str(k)+' :')
    for i in range(0, 16):
        print(int(k**i), end=' ')
    print()
        