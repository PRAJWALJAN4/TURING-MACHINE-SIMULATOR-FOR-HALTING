"""
TURING MACHINE SIMULATOR WITH GUI
This program provides:
1. A Turing Machine implementation with configurable states/transitions
2. Predefined example machines for common computational problems
3. Visual interface showing tape evolution and execution trace 
"""

import tkinter as tk
from tkinter import scrolledtext, StringVar, OptionMenu
import networkx as nx  # Currently unused - potential future feature for state graph visualization
import matplotlib.pyplot as plt  # Currently unused - potential future feature for tape plotting

class TuringMachine:
    """Core Turing Machine implementation with tape management and transition handling"""
    
    def __init__(self, states, tape_alphabet, start_state, accept_state, reject_state, transitions, input_string, max_steps=1000):
        """
        Initialize Turing Machine components:
        - states: All possible states in the state machine
        - tape_alphabet: Valid symbols allowed on the tape
        - start_state: Initial state when computation begins
        - accept/reject_state: Terminal states that halt computation
        - transitions: Dictionary mapping (state, symbol) to (new_state, write_symbol, direction)
        - input_string: Initial tape content before computation
        - max_steps: Safety limit to prevent infinite loops
        """
        self.states = states
        self.tape_alphabet = tape_alphabet
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = transitions
        self.max_steps = max_steps
        self.reset(input_string)

    def reset(self, input_string):
        """
        Initialize/reinitialize tape and machine state:
        - Creates tape as input + 50 blank symbols (_) as right buffer
        - Sets head to start position (leftmost symbol)
        - Resets step counter and transition history
        - Initializes halted status flag
        """
        self.tape = list(input_string) + ['_'] * 50  # Simulate infinite tape with buffer
        self.head = 0  # Points to current read/write position
        self.current_state = self.start_state
        self.steps = 0  # Safety counter to prevent infinite loops
        self.transition_trace = []  # History of executed transitions
        self.halted = False  # Machine status flag

    def step(self):
        """
        Execute one computation step:
        1. Check step limit and halted status
        2. Handle tape boundary conditions (extend tape if needed)
        3. Read current symbol under head
        4. Find matching transition rule
        5. Update tape, state, and head position
        6. Check for accept/reject states
        Returns: (continue_flag, status_message)
        """
        # Safety check for infinite execution prevention
        if self.steps >= self.max_steps:
            self.halted = True
            return False, f"Step limit ({self.max_steps}) reached — forced halt."

        if self.halted:
            return False, "Machine already halted"

        # Tape boundary management (simulate infinite tape)
        if self.head >= len(self.tape):
            self.tape.append('_')  # Add blank symbol to right
        if self.head < 0:
            self.tape.insert(0, '_')  # Add blank symbol to left
            self.head = 0  # Reset head position after left expansion

        # Transition lookup and execution
        symbol = self.tape[self.head]
        transition_key = f"{self.current_state}_{symbol}"

        if transition_key not in self.transitions:
            self.halted = True
            return False, f"No transition for ({self.current_state}, {symbol}) — halted."

        # Parse transition components
        next_state, write_symbol, direction = self.transitions[transition_key]
        
        # Record transition for history tracking
        self.transition_trace.append(
            f"({self.current_state}, {symbol}) → ({next_state}, {write_symbol}, {direction})"
        )

        # Update machine state
        self.tape[self.head] = write_symbol  # Write symbol to tape
        self.current_state = next_state  # Change state

        # Move head according to direction (R/L/N)
        if direction == 'R':
            self.head += 1  # Move right
        elif direction == 'L':
            self.head -= 1  # Move left
        # 'N' (no move) handled by absence of movement

        self.steps += 1  # Increment safety counter

        # Check for terminal states
        if self.current_state in [self.accept_state, self.reject_state]:
            self.halted = True

        # Return continue flag and status message
        return (not self.halted, 
                f"Step {self.steps}: State={self.current_state}, "
                f"Head={self.head}, Tape={''.join(self.tape).strip('_')}")

    def is_accepted(self):
        """Check if machine halted in accept state"""
        return self.current_state == self.accept_state

    def is_rejected(self):
        """Check if machine halted in reject state"""
        return self.current_state == self.reject_state

# =====================================================================
# PREDEFINED TURING MACHINE EXAMPLES
# =====================================================================
tm_examples = {
    "Match 0ⁿ1ⁿ (e.g. 000111)": {
        """
        Language Recognizer: {0^n1^n | n ≥ 0}
        Strategy:
        1. Cross off 0s and 1s in pairs
        2. Replace 0 with X (mark as processed)
        3. Find matching 1 and replace with Y
        4. Verify all symbols processed correctly
        """
        "states": ["q0", "q1", "q2", "q3", "halt", "reject"],
        "tape_alphabet": ["0", "1", "X", "Y", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            # Initial state processing
            "q0_0": ["q1", "X", "R"],  # Mark first 0, move right to find 1
            "q0_X": ["q0", "X", "R"],  # Skip already processed 0s
            "q0_Y": ["q3", "Y", "R"],  # All 0s processed, verify 1s
            "q0__": ["halt", "_", "N"],  # Empty string accepted
            "q0_1": ["reject", "1", "N"],  # 1 before 0 → reject
            
            # Processing 0s phase
            "q1_0": ["q1", "0", "R"],  # Move through unprocessed 0s
            "q1_Y": ["q1", "Y", "R"],  # Skip processed 1s
            "q1_1": ["q2", "Y", "L"],  # Found matching 1, mark it
            "q1__": ["reject", "_", "N"],  # No matching 1 found
            
            # Backtrack to start
            "q2_0": ["q2", "0", "L"],  # Move left through 0s
            "q2_Y": ["q2", "Y", "L"],  # Move left through processed 1s
            "q2_X": ["q0", "X", "R"],  # Return to start position
            
            # Verification phase
            "q3_Y": ["q3", "Y", "R"],  # Skip processed 1s
            "q3__": ["halt", "_", "N"],  # All symbols processed → accept
            "q3_X": ["reject", "X", "N"],  # Remaining 0 markers → reject
            "q3_0": ["reject", "0", "N"],  # Remaining 0s → reject
            "q3_1": ["reject", "1", "N"],  # Remaining 1s → reject
        }
    },
    # ... (other examples follow with similar detailed comments)
}

# =====================================================================
# GUI IMPLEMENTATION
# =====================================================================
def simulate_tm_gui():
    """
    Main simulation controller:
    1. Creates Turing Machine instance from selected example
    2. Resets GUI display elements
    3. Starts asynchronous execution loop
    """
    global tm
    # Get selected machine configuration
    tm_def = tm_examples[selected_example.get()]
    
    # Instantiate Turing Machine with user input
    tm = TuringMachine(
        states=tm_def["states"],
        tape_alphabet=tm_def["tape_alphabet"],
        start_state=tm_def["start_state"],
        accept_state=tm_def["accept_state"],
        reject_state=tm_def["reject_state"],
        transitions=tm_def["transitions"],
        input_string=entry.get(),
        max_steps=1000
    )
    
    # Clear previous results
    output_area.delete("1.0", tk.END)
    transition_area.delete("1.0", tk.END)
    verdict_label.config(text="")
    
    # Initial tape visualization
    update_tape(tm)
    
    # Start step-by-step execution with 100ms delay
    root.after(100, run_tm_step)

def run_tm_step():
    """
    Recursive step executor:
    1. Runs single step of Turing Machine
    2. Updates GUI components with new state
    3. Schedules next step if machine hasn't halted
    4. Shows final verdict when computation ends
    """
    if not tm.halted:
        # Execute one computation step
        cont, msg = tm.step()
        
        # Update output displays
        output_area.insert(tk.END, msg + "\n")
        transition_area.insert(tk.END, tm.transition_trace[-1] + "\n")
        update_tape(tm)
        
        # Continue execution if not halted
        if cont and not tm.halted:
            root.after(150, run_tm_step)  # 150ms delay between steps
        else:
            # Determine and display final result
            verdict = ("✅ Accepted" if tm.is_accepted() 
                      else "❌ Rejected" if tm.is_rejected() 
                      else "⚠️ Halted")
            verdict_label.config(text=verdict)

def update_tape(tm):
    """
    Tape visualization handler:
    1. Clears previous tape display
    2. Draws 21-cell window centered at head position
    3. Highlights current head position
    4. Shows current state below head
    """
    tape_canvas.delete("all")
    x_start = 10  # Initial drawing position
    cell_size = 30  # Pixel size per tape cell
    
    # Display cells from head-10 to head+10 (21 cells total)
    for i in range(tm.head - 10, tm.head + 11):
        # Handle tape boundaries
        symbol = "_" if i < 0 or i >= len(tm.tape) else tm.tape[i]
        
        # Calculate cell position
        x_pos = x_start + (i - tm.head + 10) * cell_size
        
        # Draw tape cell
        tape_canvas.create_rectangle(
            x_pos, 10, x_pos + cell_size, 40,
            fill="yellow" if i == tm.head else "white",  # Highlight head
            outline="black"
        )
        
        # Display cell symbol
        tape_canvas.create_text(x_pos + cell_size/2, 25, text=symbol)
        
        # Show current state under head
        if i == tm.head:
            tape_canvas.create_text(
                x_pos + cell_size/2, 55, 
                text=tm.current_state, 
                font=("Arial", 8, "italic")
            )

# =====================================================================
# GUI COMPONENT SETUP
# =====================================================================
root = tk.Tk()
root.title("Turing Machine Simulator")

# Input Section -------------------------------------------------------
tk.Label(root, text="Enter Input String:").pack()
entry = tk.Entry(root, width=30)
entry.pack()

# Machine Selection --------------------------------------------------
selected_example = StringVar(root)
selected_example.set(list(tm_examples.keys())[0])  # Default to first example
tk.Label(root, text="Select TM Language:").pack()
OptionMenu(root, selected_example, *tm_examples.keys()).pack()

# Control Button ------------------------------------------------------
tk.Button(root, text="Run Simulation", command=simulate_tm_gui).pack(pady=5)

# Output Displays -----------------------------------------------------
# Execution Log
output_area = scrolledtext.ScrolledText(root, width=70, height=8, wrap=tk.WORD)
output_area.pack(padx=10, pady=5)

# Transition History
tk.Label(root, text="Transitions:").pack()
transition_area = scrolledtext.ScrolledText(root, width=70, height=6, wrap=tk.WORD)
transition_area.pack(padx=10, pady=5)

# Final Verdict Display
verdict_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
verdict_label.pack(pady=5)

# Tape Visualization Canvas
tape_canvas = tk.Canvas(root, width=700, height=70, bg="lightgray")
tape_canvas.pack(pady=10)

# Start GUI Event Loop
root.mainloop()
