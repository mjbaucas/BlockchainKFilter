filenames = ["rssiLocal1a.txt", "rssiLocal1b.txt", "rssiLocal1c.txt", "rssiLocal1d.txt",
        "rssiLocal2a.txt", "rssiLocal2b.txt", "rssiLocal2c.txt", "rssiLocal2d.txt",
        "rssiLocal3a.txt", "rssiLocal3b.txt", "rssiLocal3c.txt", "rssiLocal3d.txt",
        "rssiLocal4a.txt", "rssiLocal4b.txt", "rssiLocal4c.txt", "rssiLocal4d.txt"]

if __name__ == "__main__":
    for filename in filenames:
        rssi_file = open(filename, "r")
        lines = rssi_file.readlines()

        acc = 0
        count = 0
        for line in lines:
            line = line.split(" ")
            acc += abs(float(line[0])-float(line[1]))/abs(float(line[0]))
            count+=1
        
        print(filename + ": " + str(1 - acc/count))