if __name__ == "__main__":
    # Taking the inputs:
    print("1) Enter the three co=ordinates of the G")
    gx=int(input("Gx"))
    gy=int(input("Gy"))
    gz=int(input("Gz"))

    print("2) GC")
    gc=int(input("GC: "))
    print("3) Size of effector scalar Note: Magnartic properties and size of the MRBot")
    effector_scalar=int(input("effector_scalar: "))

    velocity_profile=[]
    j=int(input("Enter no. of positions: "))
    for i in range(j):
        k=int(input("velocity profile at"+i+1+"th position"))
        velocity_profile.append(k)
    
    


