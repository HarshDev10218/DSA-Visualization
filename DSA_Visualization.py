import tkinter as tk
import random
import time
import math

def switch_screen(root, new_function):
    for widget in root.winfo_children():
        widget.destroy()
    new_function(root)

def Home(root):
    HomeLabel = tk.Label(root, text="Home Screen", font=("Arial", 20, "bold"))
    btn_sort = tk.Button(root, text="Sorting", font=("Arial", 16), width=15,
                         command=lambda: switch_screen(root, open_sort))
    btn_search = tk.Button(root, text="Searching", font=("Arial", 16), width=15,
                           command=lambda: switch_screen(root, open_search))

    HomeLabel.pack(pady=20)
    btn_sort.pack(pady=10)
    btn_search.pack(pady=10)

def open_sort(root):
    btn_bubble = tk.Button(root, text="Bubble Sort", font=("Arial", 16), width=15,
                           command=lambda: switch_screen(root, open_bubble))
    btn_selection = tk.Button(root, text="Selection Sort", font=("Arial", 16), width=15,
                              command=lambda: switch_screen(root, open_selection))
    btn_merge = tk.Button(root, text="Merge Sort", font=("Arial", 16), width=15,
                          command=lambda: switch_screen(root, open_merge))
    btn_insertion = tk.Button(root, text="Insertion Sort", font=("Arial", 16), width=15,
                              command=lambda: switch_screen(root, open_insertion))
    btn_quick = tk.Button(root, text="Quick Sort", font=("Arial", 16), width=15,
                          command=lambda: switch_screen(root, open_quick))
    btn_back = tk.Button(root, text="Back to Home", font=("Arial", 12, "bold"), fg="red",
                         command=lambda: switch_screen(root, Home))

    btn_bubble.pack(pady=5)
    btn_selection.pack(pady=5)
    btn_merge.pack(pady=5)
    btn_insertion.pack(pady=5)
    btn_quick.pack(pady=5)
    btn_back.pack(pady=15)

def open_search(root):
    btn_linear = tk.Button(root, text="Linear Search", font=("Arial", 16), width=15,
                           command=lambda: switch_screen(root, open_linear))
    btn_binary = tk.Button(root, text="Binary Search", font=("Arial", 16), width=15,
                           command=lambda: switch_screen(root, open_binary))
    btn_jump = tk.Button(root, text="Jump Search", font=("Arial", 16), width=15,
                         command=lambda: switch_screen(root, open_jump))
    btn_interp = tk.Button(root, text="Interpolation Search", font=("Arial", 16), width=15,
                            command=lambda: switch_screen(root, open_interpolation))
    btn_expon = tk.Button(root, text="Exponential Search", font=("Arial", 16), width=15,
                           command=lambda: switch_screen(root, open_exponential))
    btn_back = tk.Button(root, text="Back to Home", font=("Arial", 12, "bold"), fg="red",
                         command=lambda: switch_screen(root, Home))

    btn_linear.pack(pady=5)
    btn_binary.pack(pady=5)
    btn_jump.pack(pady=5)
    btn_interp.pack(pady=5)
    btn_expon.pack(pady=5)
    btn_back.pack(pady=15)

# --- CONFIGURABLE GLOBAL ENGINE CONTROLLER DASHBOARD ---
def create_control_panel(root, canvas, data, sort_callback, time_comp, space_comp, is_search=False):
    shuffles_var = tk.IntVar(value=0)
    time_var = tk.StringVar(value="0.00s")
    is_paused = [False]
    is_running = [False]
    speed_scale = [None]
    start_time = [0]
    elapsed_before_pause = [0]
    target_val = [None]

    control = {
        "shuffles": shuffles_var,
        "time": time_var,
        "is_paused": is_paused,
        "is_running": is_running,
        "speed": speed_scale,
        "start_time": start_time,
        "elapsed": elapsed_before_pause,
        "target": target_val
    }

    panel = tk.Frame(root)
    panel.pack(pady=5)

    lbl_shuffles_text = "Comparisons: 0" if is_search else "Swaps: 0"
    lbl_shuffles = tk.Label(panel, text=lbl_shuffles_text, font=("Arial", 10, "bold"))
    lbl_shuffles.grid(row=0, column=0, padx=10)
    lbl_time = tk.Label(panel, text="Time: 0.00s", font=("Arial", 10, "bold"))
    lbl_time.grid(row=0, column=1, padx=10)

    comp_frame = tk.LabelFrame(root, text="Asymptotic Complexity Metrics", font=("Arial", 9, "italic"))
    comp_frame.pack(pady=5, fill="x", padx=20)
    
    lbl_t_comp = tk.Label(comp_frame, text=f"Time Complexity: {time_comp}", font=("Arial", 10))
    lbl_t_comp.pack()
    lbl_s_comp = tk.Label(comp_frame, text=f"Space Complexity: {space_comp}", font=("Arial", 10))
    lbl_s_comp.pack()

    def draw_elements(current_data, highlights=None):
        canvas.delete("all")
        if highlights is None:
            highlights = {}
        
        num_elements = len(current_data)
        spacing = 2
        total_spacing = spacing * (num_elements - 1)
        bar_width = (280 - 10 - total_spacing) // num_elements
        
        for i, val in enumerate(current_data):
            x0 = i * (bar_width + spacing) + 5
            x1 = x0 + bar_width
            
            if is_search:
                y0 = 50
                y1 = 150
                color = highlights.get(i, "skyblue")
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="grey")
                canvas.create_text((x0 + x1) // 2, 100, text=str(val), font=("Arial", 8, "bold"))
            else:
                y0 = 200 - val
                y1 = 200
                color = highlights.get(i, "skyblue") if highlights else color
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        root.update()

    def check_pause_and_delay():
        if not is_running[0]:
            return False
        while is_paused[0]:
            if not is_running[0]:
                return False
            root.update()
            time.sleep(0.05)
            start_time[0] = time.time() - elapsed_before_pause[0]
        
        elapsed_before_pause[0] = time.time() - start_time[0]
        time_var.set(f"{elapsed_before_pause[0]:.2f}s")
        lbl_time.config(text=f"Time: {time_var.get()}")
        
        delay = int(105 - speed_scale[0].get())
        root.after(delay)
        return True

    def increment_shuffles():
        shuffles_var.set(shuffles_var.get() + 1)
        lbl_text = "Comparisons: " if is_search else "Swaps: "
        lbl_shuffles.config(text=f"{lbl_text}{shuffles_var.get()}")

    def on_start():
        if is_running[0] and is_paused[0]:
            is_paused[0] = False
            start_time[0] = time.time() - elapsed_before_pause[0]
            btn_start.config(text="Pause")
        elif not is_running[0]:
            if is_search:
                try:
                    target_val[0] = int(ent_target.get())
                except ValueError:
                    lbl_shuffles.config(text="Invalid Target")
                    return
            is_running[0] = True
            is_paused[0] = False
            shuffles_var.set(0)
            elapsed_before_pause[0] = 0
            lbl_shuffles.config(text="Comparisons: 0" if is_search else "Swaps: 0")
            lbl_time.config(text="Time: 0.00s")
            start_time[0] = time.time()
            btn_start.config(text="Pause")
            sort_callback(draw_elements, check_pause_and_delay, increment_shuffles, control)
        else:
            is_paused[0] = True
            btn_start.config(text="Resume")

    def on_reset():
        is_running[0] = False
        is_paused[0] = False
        btn_start.config(text="Sort" if not is_search else "Search")
        shuffles_var.set(0)
        elapsed_before_pause[0] = 0
        lbl_shuffles.config(text="Comparisons: 0" if is_search else "Swaps: 0")
        lbl_time.config(text="Time: 0.00s")
        
        if is_search:
            # Searching requires sorted arrays to function properly for binary variants
            data.clear()
            data.extend(sorted([random.randint(10, 99) for _ in range(12)]))
        else:
            for i in range(len(data)):
                data[i] = random.randint(10, 180)
        draw_elements(data)

    btn_start = tk.Button(panel, text="Search" if is_search else "Sort", width=8, bg="lightgreen", command=on_start)
    btn_start.grid(row=1, column=0, pady=5)
    btn_reset = tk.Button(panel, text="Reset", width=8, bg="lightcoral", command=on_reset)
    btn_reset.grid(row=1, column=1, pady=5)

    if is_search:
        lbl_ent = tk.Label(panel, text="Target Num:", font=("Arial", 9))
        lbl_ent.grid(row=2, column=0, sticky="e")
        ent_target = tk.Entry(panel, width=5)
        ent_target.insert(0, str(data[random.randint(0, len(data)-1)]))
        ent_target.grid(row=2, column=1, sticky="w")

    scale_row = 3 if is_search else 2
    scale_obj = tk.Scale(panel, from_=5, to=100, orient="horizontal", label="Speed Adjust")
    scale_obj.set(50)
    scale_obj.grid(row=scale_row, column=0, columnspan=2, sticky="ew")
    
    speed_scale[0] = scale_obj
    return draw_elements

# ==================== SORTING VISUALIZERS ====================

def open_bubble(root):
    title = tk.Label(root, text="Bubble Sort Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = [random.randint(10, 180) for _ in range(15)]

    def bubble_sort_engine(draw, check_loop, add_shuffle, control):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if not control["is_running"][0]: return
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    add_shuffle()
                    draw(data)
                    if not check_loop(): return
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, "skyblue", bubble_sort_engine, "O(n²)", "O(1)")
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_sort)).pack(pady=5)

def open_selection(root):
    title = tk.Label(root, text="Selection Sort Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = [random.randint(10, 180) for _ in range(15)]

    def selection_sort_engine(draw, check_loop, add_shuffle, control):
        n = len(data)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if not control["is_running"][0]: return
                if data[j] < data[min_idx]:
                    min_idx = j
            if min_idx != i:
                data[i], data[min_idx] = data[min_idx], data[i]
                add_shuffle()
                draw(data)
                if not check_loop(): return
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, "blue", selection_sort_engine, "O(n²)", "O(1)")
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_sort)).pack(pady=5)

def open_merge(root):
    title = tk.Label(root, text="Merge Sort Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = [random.randint(10, 180) for _ in range(15)]

    def merge_sort_engine(draw, check_loop, add_shuffle, control):
        def internal_merge(arr, start, mid, end):
            L = arr[start:mid+1]
            R = arr[mid+1:end+1]
            i = j = 0
            k = start
            while i < len(L) and j < len(R):
                if not control["is_running"][0]: return
                if L[i] <= R[j]:
                    arr[k] = L[i]; i += 1
                else:
                    arr[k] = R[j]; j += 1
                add_shuffle(); draw(data)
                if not check_loop(): return
                k += 1
            while i < len(L):
                if not control["is_running"][0]: return
                arr[k] = L[i]; i += 1; k += 1; add_shuffle(); draw(data)
                if not check_loop(): return
            while j < len(R):
                if not control["is_running"][0]: return
                arr[k] = R[j]; j += 1; k += 1; add_shuffle(); draw(data)
                if not check_loop(): return

        def divide_and_conquer(arr, start, end):
            if start < end:
                mid = (start + end) // 2
                divide_and_conquer(arr, start, mid)
                divide_and_conquer(arr, mid + 1, end)
                internal_merge(arr, start, mid, end)

        divide_and_conquer(data, 0, len(data) - 1)
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, "green", merge_sort_engine, "O(n log n)", "O(n)")
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_sort)).pack(pady=5)

def open_quick(root):
    title = tk.Label(root, text="Quick Sort Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = [random.randint(10, 180) for _ in range(15)]

    def quick_sort_engine(draw, check_loop, add_shuffle, control):
        def partition(low, high):
            pivot = data[high]
            i = low - 1
            for j in range(low, high):
                if not control["is_running"][0]: return -1
                if data[j] <= pivot:
                    i += 1
                    data[i], data[j] = data[j], data[i]
                    add_shuffle(); draw(data)
                    if not check_loop(): return -1
            data[i+1], data[high] = data[high], data[i+1]
            add_shuffle(); draw(data)
            if not check_loop(): return -1
            return i + 1

        def run_quick(low, high):
            if low < high:
                pi = partition(low, high)
                if pi == -1: return
                run_quick(low, pi - 1)
                run_quick(pi + 1, high)

        run_quick(0, len(data) - 1)
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, "purple", quick_sort_engine, "O(n log n)", "O(log n)")
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_sort)).pack(pady=5)

def open_insertion(root):
    title = tk.Label(root, text="Insertion Sort Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = [random.randint(10, 180) for _ in range(15)]

    def insertion_sort_engine(draw, check_loop, add_shuffle, control):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                if not control["is_running"][0]: return
                data[j + 1] = data[j]
                j -= 1
                add_shuffle(); draw(data)
                if not check_loop(): return
            data[j + 1] = key
            add_shuffle(); draw(data)
            if not check_loop(): return
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, "orange", insertion_sort_engine, "O(n²)", "O(1)")
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_sort)).pack(pady=5)


# ==================== SEARCHING VISUALIZERS ====================

def open_linear(root):
    title = tk.Label(root, text="Linear Search Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = sorted([random.randint(10, 99) for _ in range(12)])

    def linear_search_engine(draw, check_loop, add_comp, control):
        target = control["target"][0]
        states = {}
        for i in range(len(data)):
            if not control["is_running"][0]: return
            add_comp()
            states[i] = "yellow"
            draw(data, states)
            if not check_loop(): return
            
            if data[i] == target:
                states[i] = "green"
                draw(data, states)
                control["is_running"][0] = False
                return
            else:
                states[i] = "lightgrey"
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, linear_search_engine, "O(n)", "O(1)", is_search=True)
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_search)).pack(pady=5)

def open_binary(root):
    title = tk.Label(root, text="Binary Search Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = sorted([random.randint(10, 99) for _ in range(12)])

    def binary_search_engine(draw, check_loop, add_comp, control):
        target = control["target"][0]
        low = 0
        high = len(data) - 1
        states = {}
        
        while low <= high:
            if not control["is_running"][0]: return
            mid = (low + high) // 2
            add_comp()
            
            # Highlight current search frame boundary window split
            current_states = states.copy()
            current_states[mid] = "yellow"
            draw(data, current_states)
            if not check_loop(): return
            
            if data[mid] == target:
                states[mid] = "green"
                draw(data, states)
                control["is_running"][0] = False
                return
            elif data[mid] < target:
                for idx in range(low, mid + 1): states[idx] = "lightgrey"
                low = mid + 1
            else:
                for idx in range(mid, high + 1): states[idx] = "lightgrey"
                high = mid - 1
            draw(data, states)
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, binary_search_engine, "O(log n)", "O(1)", is_search=True)
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_search)).pack(pady=5)

def open_jump(root):
    title = tk.Label(root, text="Jump Search Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = sorted([random.randint(10, 99) for _ in range(12)])

    def jump_search_engine(draw, check_loop, add_comp, control):
        target = control["target"][0]
        n = len(data)
        step = int(math.sqrt(n))
        prev = 0
        states = {}
        
        while data[min(step, n)-1] < target:
            if not control["is_running"][0]: return
            add_comp()
            for idx in range(prev, min(step, n)): states[idx] = "lightgrey"
            prev = step
            step += int(math.sqrt(n))
            draw(data, states)
            if not check_loop(): return
            if prev >= n:
                control["is_running"][0] = False
                return
                
        while data[prev] < target:
            if not control["is_running"][0]: return
            add_comp()
            states[prev] = "lightgrey"
            prev += 1
            if prev == min(step, n):
                control["is_running"][0] = False
                return
            states[prev] = "yellow"
            draw(data, states)
            if not check_loop(): return
            
        add_comp()
        if data[prev] == target:
            states[prev] = "green"
        else:
            states[prev] = "lightgrey"
        draw(data, states)
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, jump_search_engine, "O(√n)", "O(1)", is_search=True)
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_search)).pack(pady=5)

def open_interpolation(root):
    title = tk.Label(root, text="Interpolation Search Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = sorted([random.randint(10, 99) for _ in range(12)])

    def interpolation_search_engine(draw, check_loop, add_comp, control):
        target = control["target"][0]
        low = 0
        high = len(data) - 1
        states = {}
        
        while low <= high and target >= data[low] and target <= data[high]:
            if not control["is_running"][0]: return
            add_comp()
            
            if low == high:
                if data[low] == target: states[low] = "green"
                else: states[low] = "lightgrey"
                draw(data, states)
                break
                
            # Proportional parsing probe formula matching distribution index location
            pos = low + int(((float(high - low) / (data[high] - data[low])) * (target - data[low])))
            
            if pos < low or pos > high:
                break
                
            current_states = states.copy()
            current_states[pos] = "yellow"
            draw(data, current_states)
            if not check_loop(): return
            
            if data[pos] == target:
                states[pos] = "green"
                draw(data, states)
                control["is_running"][0] = False
                return
            elif data[pos] < target:
                for idx in range(low, pos + 1): states[idx] = "lightgrey"
                low = pos + 1
            else:
                for idx in range(pos, high + 1): states[idx] = "lightgrey"
                high = pos - 1
            draw(data, states)
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, interpolation_search_engine, "Avg: O(log log n), Worst: O(n)", "O(1)", is_search=True)
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_search)).pack(pady=5)

def open_exponential(root):
    title = tk.Label(root, text="Exponential Search Visualizer", font=("Arial", 14, "bold"))
    title.pack(pady=5)
    canvas = tk.Canvas(root, width=280, height=200, bg="white")
    canvas.pack(pady=5)
    data = sorted([random.randint(10, 99) for _ in range(12)])

    def exponential_search_engine(draw, check_loop, add_comp, control):
        target = control["target"][0]
        n = len(data)
        states = {}
        
        add_comp()
        states[0] = "yellow"
        draw(data, states)
        if not check_loop(): return
        
        if data[0] == target:
            states[0] = "green"
            draw(data, states)
            control["is_running"][0] = False
            return
            
        states[0] = "lightgrey"
        bound = 1
        while bound < n and data[bound] <= target:
            if not control["is_running"][0]: return
            add_comp()
            for idx in range(0, bound): states[idx] = "lightgrey"
            states[bound] = "yellow"
            draw(data, states)
            if not check_loop(): return
            bound *= 2
            
        # Binary bounds segment isolation
        low = bound // 2
        high = min(bound, n - 1)
        
        while low <= high:
            if not control["is_running"][0]: return
            mid = (low + high) // 2
            add_comp()
            
            current_states = states.copy()
            current_states[mid] = "yellow"
            draw(data, current_states)
            if not check_loop(): return
            
            if data[mid] == target:
                states[mid] = "green"
                draw(data, states)
                control["is_running"][0] = False
                return
            elif data[mid] < target:
                for idx in range(low, mid + 1): states[idx] = "lightgrey"
                low = mid + 1
            else:
                for idx in range(mid, high + 1): states[idx] = "lightgrey"
                high = mid - 1
            draw(data, states)
        control["is_running"][0] = False

    draw_init = create_control_panel(root, canvas, data, exponential_search_engine, "O(log n)", "O(1)", is_search=True)
    draw_init(data)
    tk.Button(root, text="Back to Menu", command=lambda: switch_screen(root, open_search)).pack(pady=5)

def main():
    root = tk.Tk()
    root.title("DSA Visualization")
    root.geometry("340x660") 
    Home(root)
    root.mainloop()

if __name__ == "__main__" :
    main()
