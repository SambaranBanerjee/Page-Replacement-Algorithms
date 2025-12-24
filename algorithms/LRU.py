def search(key, fr):
    """Search for key in frame list"""
    for i in range(len(fr)):
        if fr[i] == key:
            return i  # Return index if found
    return -1  # Return -1 if not found

def lruPage(pg, fn, return_steps=False):
    """LRU Page Replacement Algorithm"""
    pn = len(pg)
    fr = []  # Frames
    time = []  # Time of last use for each frame
    hit = 0
    miss = 0
    steps = []  # To store step-by-step execution
    counter = 0
    
    print(f"\nLRU Algorithm")
    print(f"Number of frames: {fn}")
    print(f"Page reference string: {pg}")
    print("-" * 50)
    
    for i in range(pn):
        counter += 1
        current_step = {
            'step': i + 1,
            'page': pg[i],
            'frames_before': fr.copy(),
            'time_before': time.copy(),
            'hit': False,
            'fault': False,
            'replaced': None,
            'frames_after': None,
            'time_after': None
        }
        
        index = search(pg[i], fr)
        
        if index != -1:  # Page found in frames (hit)
            hit += 1
            current_step['hit'] = True
            time[index] = counter  # Update last used time
            current_step['frames_after'] = fr.copy()
            current_step['time_after'] = time.copy()
        else:  # Page fault
            miss += 1
            current_step['fault'] = True
            
            if len(fr) < fn:  # If frames are not full
                fr.append(pg[i])
                time.append(counter)
                current_step['frames_after'] = fr.copy()
                current_step['time_after'] = time.copy()
            else:  # Need to replace a page
                # Find LRU page (minimum time)
                lru_index = time.index(min(time))
                current_step['replaced'] = fr[lru_index]
                fr[lru_index] = pg[i]
                time[lru_index] = counter
                current_step['frames_after'] = fr.copy()
                current_step['time_after'] = time.copy()
        
        steps.append(current_step)
        
        # Print step information
        print(f"Step {i+1}: Page {pg[i]} -> ", end="")
        if current_step['hit']:
            print(f"Hit - Frames: {current_step['frames_before']}")
        else:
            print(f"Fault - Frames: {current_step['frames_before']} -> {current_step['frames_after']}", end="")
            if current_step['replaced']:
                print(f" (Replaced: {current_step['replaced']})")
            else:
                print()
    
    print("-" * 50)
    print(f"Total Hits: {hit}")
    print(f"Total Misses (Page Faults): {miss}")
    print(f"Hit Ratio: {hit/pn:.2%}")
    print(f"Fault Ratio: {miss/pn:.2%}")
    
    if return_steps:
        return hit, miss, steps
    else:
        return hit, miss

# For direct testing
if __name__ == "__main__":
    fn = int(input("Enter the number of frames: "))
    pg_input = input("Enter the page reference string (space-separated integers): ")
    pg = list(map(int, pg_input.split()))
    
    hit, miss, steps = lruPage(pg, fn)