import os 
j= 0
for i in os.listdir("data/testset"):
    print(i)
    path = f"data/testset/{i}"
    dest = f"data/testset/{j}.jpg"
    os.rename(path,dest)
    j += 1
