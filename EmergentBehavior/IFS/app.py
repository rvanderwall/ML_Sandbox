from Animator import Animator
from IFS_Samples import dragon
from IFS import IFS

if __name__ == "__main__":
    print("IFS simulator")
    ifs = IFS(dragon)
    a = Animator(ifs)
    a.run()
