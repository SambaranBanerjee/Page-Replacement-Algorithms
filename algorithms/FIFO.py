def search(key, fr):
    """Search for key in frame list"""
    for i in range(len(fr)):
        if fr[i] == key:
            return True
    return False

def fifoPage(pg, fn, return_steps=False):
    """FIFO Page Replacement Algorithm"""
    pn = len(pg)
    fr = []
    hit = 0
    miss = 0
    steps = []  # To store step-by-step execution
    
    print(f"\nFIFO Algorithm")
    print(f"Number of frames: {fn}")
    print(f"Page reference string: {pg}")
    print("-" * 50)
    
    for i in range(pn):
        current_step = {
            'step': i + 1,
            'page': pg[i],
            'frames_before': fr.copy(),
            'hit': False,
            'fault': False,
            'replaced': None,
            'frames_after': None
        }
        
        if search(pg[i], fr):
            hit += 1
            current_step['hit'] = True
            current_step['frames_after'] = fr.copy()
        else:
            miss += 1
            current_step['fault'] = True
            
            if len(fr) < fn:
                fr.append(pg[i])
                current_step['frames_after'] = fr.copy()
            else:
                # Remove first page (oldest)
                replaced = fr.pop(0)
                fr.append(pg[i])
                current_step['replaced'] = replaced
                current_step['frames_after'] = fr.copy()
        
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
    
    hit, miss, steps = fifoPage(pg, fn)