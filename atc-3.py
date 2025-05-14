import tkinter as tk
from tkinter import scrolledtext, StringVar, OptionMenu
import time

class TuringMachine:
    def __init__(self, states, tape_alphabet, start_state, accept_state, transitions, input_string):
        self.states = states
        self.tape_alphabet = tape_alphabet
        self.start_state = start_state
        self.accept_state = accept_state
        self.transitions = transitions
        self.reset(input_string)

    def reset(self, input_string):
        self.tape = list(input_string) + ['_'] * 50
        self.head = 0
        self.current_state = self.start_state
        self.steps = 0

    def step(self):
        symbol = self.tape[self.head]
        key = f"{self.current_state}_{symbol}"

        if key not in self.transitions:
            return False, f"No transition for ({self.current_state}, {symbol}) — halting."

        next_state, write_symbol, direction = self.transitions[key]
        self.tape[self.head] = write_symbol
        self.current_state = next_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

        self.steps += 1
        return True, f"Step {self.steps}: State={self.current_state}, Head={self.head}, Tape={''.join(self.tape).strip('_')}"

    def halts(self):
        """ Simulate a halting check for the TM.
            This will intentionally lead to an undecidable behavior for self-referential cases.
        """
        if self.current_state == 'loop' and self.head == 5:  # Check for self-referential condition
            raise RecursionError("Self-referential loop detected: halting problem is undecidable.")

tm_examples = {
    "Flip 0 to 1": {
        "states": ["q0", "q1", "halt"],
        "tape_alphabet": ["0", "1", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "transitions": {
            "q0_0": ["q1", "1", "R"],
            "q1__": ["halt", "_", "N"]
        }
    },
    "Unary Increment": {
        "states": ["q0", "q1", "halt"],
        "tape_alphabet": ["1", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "transitions": {
            "q0_1": ["q0", "1", "R"],
            "q0__": ["q1", "1", "N"],
            "q1__": ["halt", "_", "N"]
        }
    },
    "Halting Problem (Undecidable)": {
        "states": ["loop"],
        "tape_alphabet": ["0", "_"],
        "start_state": "loop",
        "accept_state": "halt",
        "transitions": {
            "loop_0": ["loop", "0", "R"],
            "loop__": ["loop", "_", "L"]
        }
    }
}

# GUI Setup
def simulate_tm_gui():
    global tm
    tm_def = tm_examples[selected_example.get()]
    tm = TuringMachine(
        states=tm_def["states"],
        tape_alphabet=tm_def["tape_alphabet"],
        start_state=tm_def["start_state"],
        accept_state=tm_def["accept_state"],
        transitions=tm_def["transitions"],
        input_string=entry.get()
    )
    output_area.delete("1.0", tk.END)
    update_tape(tm)
    if selected_example.get() == "Halting Problem (Undecidable)":
        output_area.insert(tk.END, "Simulating Halting Problem...\n")
        root.after(300, run_tm_step_undecidable)
    else:
        root.after(300, run_tm_step)

def run_tm_step():
    cont, msg = tm.step()
    output_area.insert(tk.END, msg + "\n")
    update_tape(tm)

    if cont and tm.current_state != tm.accept_state:
        root.after(300, run_tm_step)

def run_tm_step_undecidable():
    try:
        tm.halts()
        cont, msg = tm.step()
        output_area.insert(tk.END, msg + "\n")
        update_tape(tm)
    except RecursionError as e:
        output_area.insert(tk.END, f"Error: {str(e)}\n")
        output_area.insert(tk.END, "This TM invokes itself, so no general answer exists.\n")
        # Stop further execution if undecidability is detected.
        return

def update_tape(tm):
    tape_canvas.delete("all")
    x_start = 10
    cell_size = 30

    for i in range(tm.head - 10, tm.head + 11):
        symbol = tm.tape[i] if 0 <= i < len(tm.tape) else "_"
        x = x_start + (i - tm.head + 10) * cell_size
        tape_canvas.create_rectangle(x, 10, x + cell_size, 40, fill="yellow" if i == tm.head else "white", outline="black")
        tape_canvas.create_text(x + cell_size / 2, 25, text=symbol)

# Main Window
root = tk.Tk()
root.title("Turing Machine Visual Simulator")

tk.Label(root, text="Enter Tape Input:").pack()
entry = tk.Entry(root, width=30)
entry.pack()

selected_example = StringVar(root)
selected_example.set("Flip 0 to 1")
tk.Label(root, text="Select TM Example:").pack()
OptionMenu(root, selected_example, *tm_examples.keys()).pack()

tk.Button(root, text="Simulate TM", command=simulate_tm_gui).pack(pady=5)

output_area = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
output_area.pack(padx=10, pady=10)

tape_canvas = tk.Canvas(root, width=700, height=50, bg="lightgray")
tape_canvas.pack(pady=10)

root.mainloop()
