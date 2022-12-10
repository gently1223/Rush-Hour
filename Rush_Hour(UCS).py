import time

#Get the fuel level of all cars from the current pattern.
def getFuel(pattern):
    txt = pattern.split(' ')
    fuel = {}
    for c in txt[0]:
        if c.isupper():
            fuel[c] = 100
    for i in range(1, len(txt)):
        if len(txt[i]) == 0:
            continue
        f = 0
        for j in range(1, len(txt[i])):
            f = f * 10 + ord(txt[i][j]) - ord('0')
        fuel[txt[i][0]] = f
    return fuel

#Only the parking lot model is exposed from the current pattern.
def getGrid(pattern):
    return pattern.split(' ')[0]

#Obtains whether or not the transport means v can move 
#vertically by s in the current pattern.
def canCol(pattern, v, s):
    if s == 0:
        return False
    c = 0
    rmin = -1
    rmax = -1
    for i in range(36):
        if pattern[i] == v:
            if i > 0 and pattern[i - 1] == pattern[i]:
                return False
            c = i % 6
            if rmin == -1:
                rmin = int(i / 6)
            rmax = int(i / 6)
    if rmin + s < 0:
        return False
    if rmax + s > 5:
        return False
    for i in range(36):
        if pattern[i] != v and pattern[i] != '.' and i % 6 == c and min(rmin, rmin + s) <= int(i / 6) and int(i / 6) <= max(rmax, rmax + s):
            return False
    return True

#In the current pattern, the transport means v moves 
#vertically by s and then the pattern is obtained.
def goCol(pattern, v, s):
    ans = pattern
    c = 0
    rmin = -1
    rmax = -1
    for i in range(36):
        if pattern[i] == v:
            if i > 0 and pattern[i - 1] == pattern[i]:
                return False
            c = i % 6
            if rmin == -1:
                rmin = int(i / 6)
            rmax = int(i / 6)
    ans = list(ans)
    for i in range(36):
        if ans[i] == v:
            ans[i] = '.'
    for i in range(36):
        if i % 6 == c and rmin + s <= int(i / 6) and int(i / 6) <= rmax + s:
            ans[i] = v
    ans = "".join(ans)
    return ans

#Same with canCol.
def canRow(pattern, v, s):
    if s == 0:
        return False
    r = 0
    cmin = -1
    cmax = -1
    for i in range(36):
        if pattern[i] == v:
            if i > 5 and pattern[i - 6] == pattern[i]:
                return False
            r = int(i / 6)
            if cmin == -1:
                cmin = i % 6
            cmax = i % 6
    if cmin + s < 0:
        return False
    if cmax + s > 5:
        return False
    for i in range(36):
        if pattern[i] != v and pattern[i] != '.':
            if int(i / 6) == r and min(cmin, cmin + s) <= i % 6 and i % 6 <= max(cmax, cmax + s):
                return False
    return True

#Same with goCol.
def goRow(pattern, v, s):
    ans = pattern
    r = 0
    cmin = -1
    cmax = -1
    for i in range(36):
        if pattern[i] == v:
            if i > 5 and pattern[i - 6] == pattern[i]:
                return False
            r = int(i / 6)
            if cmin == -1:
                cmin = i % 6
            cmax = i % 6
    ans = list(ans)
    for i in range(36):
        if ans[i] == v:
            ans[i]= "."
    for i in range(36):
        if int(i / 6) == r and cmin + s <= i % 6 and i % 6 <= cmax + s:
            ans[i] = v
    ans = "".join(ans)
    return ans

#Solve the problem using the Uniform Cost Search algorithm.
def SolveUCS(pattern, testCase):
    beg = float(time.time())
    fuel = getFuel(pattern)
    S = f"usc-sol-{testCase}.txt"
    G = open(S, "w")
    G.write("--------------------------------------------------------------------------------\n\n")
    G.write("Initial board configuration: ")
    G.write(pattern + "\n\n")
    G.write("!\n")
    for i in range(6):
        for j in range(6):
            G.write(pattern[i * 6 + j])
        G.write("\n")
    G.write("\n")
    G.write("Car fuel available: ")
    start = 0
    for i in fuel:
        if start == 1:
            G.write(", ")
        G.write(i)
        G.write(":")
        G.write(f"{fuel[i]}")
        start = 1
    G.write("\n")
    S = f"ucs-search-{testCase}.txt"
    H = open(S, "w")
    Q = [pattern]
    st = {}
    st[getGrid(pattern)] = 0
    searchPathLength = 0
    solutionPathLength = 0
    memSol = {}
    memSol[getGrid(pattern)] = "Begin"
    finalState = ""
    while len(Q) > 0:
        searchPathLength += 1
        if searchPathLength > 7000:
           Q.pop(0)
           continue
        p = Q[0]
        dist = st[getGrid(p)]
        H.write(f"{dist} {dist} 0 {p}\n")
        if p[17] == 'A':
            finalState = p
            solutionPathLength = dist
            break;
        Q.pop(0)
        fuel = getFuel(p)
        p = getGrid(p)
        for V in fuel:
            if fuel[V] == 0:
               continue
            for i in range(-5, 6):
                if canCol(p, V, i):
                    tmp = goCol(p, V, i)
                    for k in fuel:
                        if k == V:
                            fuel[k] = fuel[k] - 1
                        if fuel[k] < 100:
                            tmp = tmp + " "
                            tmp = tmp + k
                            tmp = tmp + str(fuel[k])
                        if k == V:
                            fuel[k] = fuel[k] + 1
                    if (getGrid(tmp) in st) == False:
                        st[getGrid(tmp)] = dist + 1
                        if i < 0:
                            memSol[getGrid(tmp)] = f"{V} up {-i}"
                        else:
                            memSol[getGrid(tmp)] = f"{V} down {i}"
                        Q.append(tmp)
                if canRow(p, V, i):
                    tmp = goRow(p, V, i)
                    for k in fuel:
                        if k == V:
                            fuel[k] = fuel[k] - 1
                        if fuel[k] < 100:
                            tmp = tmp + " "
                            tmp = tmp + k
                            tmp = tmp + str(fuel[k])
                        if k == V:
                            fuel[k] = fuel[k] + 1
                    if (getGrid(tmp) in st) == False:
                        st[getGrid(tmp)] = dist + 1
                        if i < 0:
                            memSol[getGrid(tmp)] = f"{V} left {-i}"
                        else:
                            memSol[getGrid(tmp)] = f"{V} right {i}"
                        Q.append(tmp)
    
    if len(Q) == 0:
        G.write("Sorry, could not solve the puzzle as specified.\nError: no solution found\n")
        end = float(time.time())
        t = end - beg
        t = float(int(t * 100)) / 100
        G.write(f"\nRuntime: {t} seconds\n")
    else:
        end = float(time.time())
        t = end - beg
        t = float(int(t * 100)) / 100
        G.write(f"\nRuntime: {t} seconds\n")
        G.write(f"Search path length: {searchPathLength} states\n")
        G.write(f"Solution path length: {solutionPathLength} moves\n")
        solutionPath = []
        impleState = []
        finalFuel = getFuel(finalState)
        finalGrid = getGrid(finalState)
        while memSol[getGrid(finalState)] != "Begin":
            ope = memSol[getGrid(finalState)]
            move = ope.split(' ')
            solutionPath.append(ope)
            curFuel = getFuel(finalState)
            impleState.append(ope + "    " + str(curFuel[move[0]]) + finalState)
            curFuel[move[0]] += 1
            
            if curFuel[move[0]] == 100:
                curFuel.pop(move[0])
            if(move[1][0] == 'u'):
                finalState = goCol(getGrid(finalState), move[0], int(move[2]))
            if(move[1][0] == 'd'):
                finalState = goCol(getGrid(finalState), move[0], -int(move[2]))
            if(move[1][0] == 'l'):
                finalState = goRow(getGrid(finalState), move[0], int(move[2]))
            if(move[1][0] == 'r'):
                finalState = goRow(getGrid(finalState), move[0], -int(move[2]))
            for i in curFuel:
                if curFuel[i] == 100:
                    continue
                finalState = finalState + " " + i + str(curFuel[i])
        
        G.write("Solution path:")
        SJ = 0
        for i in range(len(solutionPath) - 1, -1, -1):
            if SJ == 1:
                G.write(";")
            G.write(" " + solutionPath[i])
            SJ = 1
        G.write("\n\n")
        for i in range(len(impleState) - 1, -1, -1):
            G.write(impleState[i])
            G.write("\n")
        G.write("\n")
        
        G.write("!")
        for i in finalFuel:
            if finalFuel[i] == 100:
                continue
            G.write(" " + i + str(finalFuel[i]))
        G.write("\n")
        for i in range(6):
            for j in range(6):
                G.write(finalGrid[i * 6 + j])
            G.write("\n")
        G.write("\n")
        
        
    G.write("--------------------------------------------------------------------------------\n\n")


F = open("sample-input.txt", "r")

Data = F.read()

Data = Data.split("\n")

count = 1

for S in Data:
    if len(S) == 0:
        continue
    if S[0] == '#':
        continue
    SolveUCS(S, count)
    count += 1

