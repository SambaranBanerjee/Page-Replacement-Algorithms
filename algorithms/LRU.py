def search(key, fr):
    for i in range(len(fr)):
        if fr[i] == key:
            return True
    return False


def lruPage(pg, pn, fn):
    fr = []
    time = [0] * fn
    hit = 0
    counter = 0

    for i in range(pn):
        counter += 1

        if search(pg[i], fr):
            hit += 1
            for j in range(len(fr)):
                if fr[j] == pg[i]:
                    time[j] = counter
            continue

        if len(fr) < fn:
            fr.append(pg[i])
            time[len(fr) - 1] = counter
        else:
            lru_index = time.index(min(time))
            fr[lru_index] = pg[i]
            time[lru_index] = counter

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

lruPage(pg, pn, fn)
