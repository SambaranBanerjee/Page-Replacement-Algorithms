from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
import io
import base64

# Add algorithms directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

try:
    # We will use the internal simulation for consistency with the frontend table
    from algorithms.plot import graphPlot
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"Import Error: {e}")

app = Flask(__name__)
CORS(app)

@app.route("/")
def serve_frontend():
    return render_template("index.html")

@app.route("/api/calculate", methods=["POST"])
def calculate_page_faults():
    """API endpoint to calculate page faults and return step history"""
    try:
        data = request.get_json()
        
        # 1. Validate input
        frames = int(data.get('frames', 3))
        reference_string = data.get('reference_string', '')
        
        if not reference_string:
            return jsonify({'success': False, 'error': 'Reference string is required'}), 400
        
        try:
            pages = list(map(int, reference_string.split()))
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid format'}), 400
        
        if frames < 1:
            return jsonify({'success': False, 'error': 'Frames must be >= 1'}), 400
        
        # 2. Get selected algorithms
        selected_algorithms = data.get('algorithms', ['fifo', 'lru', 'optimal'])
        
        results = {}
        faults_data = {}
        
        # 3. Run simulations for each algorithm
        for algo_key in selected_algorithms:
            # We use get_algorithm_steps to get BOTH the count AND the history
            # This ensures the frontend table works
            steps = get_algorithm_steps(pages, frames, algo_key)
            
            # Calculate stats from the steps
            fault_count = sum(1 for step in steps if step['fault'])
            
            # Map frontend keys (fifo -> FIFO) for display
            display_name = algo_key.upper()
            if algo_key == 'optimal': display_name = 'Optimal'
            
            results[display_name] = {
                'name': display_name,
                'page_faults': fault_count,
                'page_fault_rate': fault_count / len(pages) if pages else 0,
                'history': steps, # CRITICAL: Frontend needs this key!
                'total': len(pages)
            }
            
            faults_data[display_name] = fault_count

        # 4. Generate comparison graph
        graph_base64 = generate_comparison_graph(faults_data)
        
        return jsonify({
            'success': True,
            'results': results, # Now contains history inside each algo
            'graph': graph_base64,
            'input': {
                'frames': frames,
                'reference_string': reference_string,
                'total_pages': len(pages)
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# --- SIMULATION LOGIC ---

def get_algorithm_steps(pages, frames, algorithm):
    """Simulates the algorithm and returns step-by-step history"""
    steps = []
    memory = []
    
    # Helper to create step object
    def record_step(step_idx, page, current_mem, is_fault, replaced_val=None):
        return {
            'step': step_idx + 1,
            'page': page,
            'memory': list(current_mem), # Copy list
            'fault': is_fault,
            'replaced': replaced_val
        }

    # --- FIFO ---
    if algorithm == 'fifo':
        queue = [] # To track arrival order
        for i, page in enumerate(pages):
            is_fault = False
            replaced = None
            
            if page not in memory:
                is_fault = True
                if len(memory) < frames:
                    memory.append(page)
                    queue.append(page)
                else:
                    replaced = queue.pop(0)
                    memory[memory.index(replaced)] = page
                    queue.append(page)
            
            steps.append(record_step(i, page, memory, is_fault, replaced))

    # --- LRU ---
    elif algorithm == 'lru':
        recent_usage = [] 
        for i, page in enumerate(pages):
            is_fault = False
            replaced = None
            
            if page not in memory:
                is_fault = True
                if len(memory) < frames:
                    memory.append(page)
                else:
                    # Find LRU page (first element in recent_usage that is in memory)
                    replaced = recent_usage[0]
                    memory[memory.index(replaced)] = page
                    recent_usage.pop(0) # Remove from usage history
            else:
                # Update usage: remove current position, add to end
                if page in recent_usage:
                    recent_usage.remove(page)
            
            recent_usage.append(page) # Mark as recently used
            steps.append(record_step(i, page, memory, is_fault, replaced))

    # --- OPTIMAL ---
    elif algorithm == 'optimal':
        for i, page in enumerate(pages):
            is_fault = False
            replaced = None
            
            if page not in memory:
                is_fault = True
                if len(memory) < frames:
                    memory.append(page)
                else:
                    # Find page that will not be used for longest time
                    farthest_idx = -1
                    victim = -1
                    
                    for mem_page in memory:
                        try:
                            # Search in future pages
                            next_use = pages[i+1:].index(mem_page)
                        except ValueError:
                            # Not found in future = infinity
                            next_use = float('inf')
                        
                        if next_use > farthest_idx:
                            farthest_idx = next_use
                            victim = mem_page
                    
                    replaced = victim
                    memory[memory.index(victim)] = page
            
            steps.append(record_step(i, page, memory, is_fault, replaced))

    return steps

def generate_comparison_graph(faults_data):
    try:
        algorithms = list(faults_data.keys())
        faults = list(faults_data.values())
        
        # Create a new figure here
        plt.figure(figsize=(10, 6))
        
        # Call the imported plot function
        graphPlot(algorithms, faults)
        
        # Save
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        return graph_base64
    except Exception as e:
        print(f"Graph Error: {e}")
        return None

# Other routes...
@app.route("/api/algorithms", methods=["GET"])
def get_algorithms_info():
    # (Keep your existing code for this function)
    return jsonify({
        'fifo': {'name': 'FIFO', 'description': 'First In First Out'},
        'lru': {'name': 'LRU', 'description': 'Least Recently Used'},
        'optimal': {'name': 'Optimal', 'description': 'Look ahead to maximize hits'}
    })

@app.route("/api/random", methods=["GET"])
def generate_random_input():
    import random
    length = request.args.get('length', 15, type=int)
    pages = [random.randint(0, 9) for _ in range(length)]
    return jsonify({
        'reference_string': ' '.join(map(str, pages)),
        'frames': random.randint(3, 5)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)