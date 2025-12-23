def search(key, fr):
    for i in range(len(fr)):
        if (fr[i] == key):
            return True
    return False

def predict(pg, fr, pn, index):
    res = -1
    farthest = index
    for i in range(len(fr)):
        j = 0
        for j in range(index, pn):
            if (fr[i] == pg[j]):
                if (j > farthest):
                    farthest = j
                    res = i
                break
        if (j == pn):
            return i
    return 0 if (res == -1) else res

def optimalPage(pg, pn, fn):
    fr = []
    hit = 0
    for i in range(pn):
        if search(pg[i], fr):
            hit += 1
            continue
        if len(fr) < fn:
            fr.append(pg[i])
        else:
            j = predict(pg, fr, pn, i + 1)
            fr[j] = pg[i]
    
    miss = pn - hit    
    print("No. of hits =", hit)
    print("No. of misses =", miss)
    return hit, miss

fn = int(input("Enter the number of frames: "))

pg_input = input("Enter the page reference string (space-separated integers): ")
pg = list(map(int, pg_input.split()))
pn = len(pg)

print(f"Page reference string: {pg}")
print(f"Number of frames: {fn}")

optimalPage(pg, pn, fn)
