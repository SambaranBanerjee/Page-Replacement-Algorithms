def search(key, fr):
    """Search for key in frame list"""
    for i in range(len(fr)):
        if fr[i] == key:
            return i  # Return index if found
    return -1  # Return -1 if not found

def optimalPage(pg, fn, return_steps=False):
    """Optimal Page Replacement Algorithm"""
    pn = len(pg)
    fr = []  # Frames
    hit = 0
    miss = 0
    steps = []  # To store step-by-step execution
    
    print(f"\nOptimal Algorithm")
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
        
        index = search(pg[i], fr)
        
        if index != -1:  # Page found in frames (hit)
            hit += 1
            current_step['hit'] = True
            current_step['frames_after'] = fr.copy()
        else:  # Page fault
            miss += 1
            current_step['fault'] = True
            
            if len(fr) < fn:  # If frames are not full
                fr.append(pg[i])
                current_step['frames_after'] = fr.copy()
            else:  # Need to replace a page
                # Find page that won't be used for longest time in future
                farthest = -1
                replace_index = -1
                
                for j in range(len(fr)):
                    # Find next occurrence of this page in future
                    next_use = float('inf')
                    for k in range(i + 1, pn):
                        if fr[j] == pg[k]:
                            next_use = k
                            break
                    
                    # If page is not used in future, replace it
                    if next_use == float('inf'):
                        replace_index = j
                        break
                    # Find the page with farthest next use
                    elif next_use > farthest:
                        farthest = next_use
                        replace_index = j
                
                current_step['replaced'] = fr[replace_index]
                fr[replace_index] = pg[i]
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
    
    hit, miss, steps = optimalPage(pg, fn)