def search(key, fr):
    for i in range(len(fr)):
        if fr[i] == key:
            return True
    return False

def fifoPage(pg, pn, fn):
    fr = []
    hit = 0
    next_replace = 0  # index of the frame to replace (oldest)

    for i in range(pn):
        if search(pg[i], fr):
            hit += 1
            continue
        if len(fr) < fn:
            fr.append(pg[i])
        else:
            # replace the oldest page (FIFO)
            fr[next_replace] = pg[i]
            next_replace = (next_replace + 1) % fn

    miss = pn - hit
    print("No. of hits =", hit)
    print("No. of misses =", miss)
    return hit, miss

if __name__ == "__main__":
    fn = int(input("Enter the number of frames: "))

    pg_input = input("Enter the page reference string (space-separated integers): ")
    pg = list(map(int, pg_input.split()))
    pn = len(pg)

    print(f"Page reference string: {pg}")
    print(f"Number of frames: {fn}")

    fifoPage(pg, pn, fn)