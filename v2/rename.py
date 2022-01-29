import os 
j= 0
for i in os.listdir("data/raw"):
    path = f"data/raw/{i}"
    dest = f"data/raw/{j}.jpg"
    os.rename(path,dest)
    j += 1
