import tkinter as tk
from tkinter import scrolledtext, StringVar, OptionMenu

class TuringMachine:
    def __init__(self, states, tape_alphabet, start_state, accept_state, reject_state, transitions, input_string, max_steps=1000):
        self.states = states
        self.tape_alphabet = tape_alphabet
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = transitions
        self.max_steps = max_steps
        self.reset(input_string)

    def reset(self, input_string):
        self.tape = list(input_string) + ['_'] * 50
        self.head = 0
        self.current_state = self.start_state
        self.steps = 0
        self.transition_trace = []
        self.halted = False

    def step(self):
        if self.steps >= self.max_steps:
            self.halted = True
            return False, f"Step limit ({self.max_steps}) reached — forced halt."
        
        if self.halted:
            return False, "Machine already halted"

        symbol = self.tape[self.head]
        key = f"{self.current_state}_{symbol}"

        if key not in self.transitions:
            self.halted = True
            return False, f"No transition for ({self.current_state}, {symbol}) — halted."

        next_state, write_symbol, direction = self.transitions[key]
        self.transition_trace.append(f"({self.current_state}, {symbol}) → ({next_state}, {write_symbol}, {direction})")

        self.tape[self.head] = write_symbol
        self.current_state = next_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

        self.steps += 1
        
        if self.current_state in [self.accept_state, self.reject_state]:
            self.halted = True
            
        return not self.halted, f"Step {self.steps}: State={self.current_state}, Head={self.head}, Tape={''.join(self.tape).strip('_')}"

    def is_accepted(self):
        return self.current_state == self.accept_state

    def is_rejected(self):
        return self.current_state == self.reject_state


# TM Definitions with explicit accept/reject states
tm_examples = {
    "Flip 0 to 1": {
        "states": ["q0", "q1", "halt", "reject"],
        "tape_alphabet": ["0", "1", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            "q0_0": ["q1", "1", "R"],
            "q1__": ["halt", "_", "N"],
            "q1_0": ["reject", "0", "N"]  # Example reject case
        }
    },
    "Unary Increment": {
        "states": ["q0", "q1", "halt", "reject"],
        "tape_alphabet": ["1", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            "q0_1": ["q0", "1", "R"],
            "q0__": ["q1", "1", "N"],
            "q1__": ["halt", "_", "N"]
        }
    },
    "Halting Problem": {
        "states": ["simulate", "halt", "reject"],
        "tape_alphabet": ["0", "1", "_"],
        "start_state": "simulate",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            "simulate_0": ["simulate", "0", "R"],
            "simulate_1": ["simulate", "1", "R"],
            "simulate__": ["simulate", "_", "R"]  # Infinite loop
        }
    }
}

# GUI Code
def simulate_tm_gui():
    global tm
    tm_def = tm_examples[selected_example.get()]
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
    output_area.delete("1.0", tk.END)
    transition_area.delete("1.0", tk.END)
    verdict_label.config(text="")
    update_tape(tm)
    root.after(100, run_tm_step)

def run_tm_step():
    if not tm.halted:
        cont, msg = tm.step()
        output_area.insert(tk.END, msg + "\n")
        update_tape(tm)
        
        if cont and not tm.halted:
            root.after(100, run_tm_step)
        else:
            transition_area.insert(tk.END, "\n".join(tm.transition_trace))
            if tm.is_accepted():
                verdict = "✅ Accepted (halt state reached)"
            elif tm.is_rejected():
                verdict = "❌ Rejected (reject state reached)"
            else:
                if tm.steps >= tm.max_steps:
                    verdict = "⚠️ Step limit exceeded (possible infinite loop)"
                else:
                    verdict = "⚠️ Halted (no transition)"
            verdict_label.config(text=verdict)

def update_tape(tm):
    tape_canvas.delete("all")
    x_start = 10
    cell_size = 30

    for i in range(tm.head - 10, tm.head + 11):
        if i < 0 or i >= len(tm.tape):
            symbol = "_"
        else:
            symbol = tm.tape[i]
            
        x = x_start + (i - tm.head + 10) * cell_size
        tape_canvas.create_rectangle(x, 10, x + cell_size, 40, 
                                   fill="yellow" if i == tm.head else "white", 
                                   outline="black")
        tape_canvas.create_text(x + cell_size/2, 25, text=symbol)
        
        if i == tm.head:
            tape_canvas.create_text(x + cell_size/2, 55, text=tm.current_state, 
                                   font=("Arial", 8, "italic"))

# Main Window Setup
root = tk.Tk()
root.title("Turing Machine Simulator with Halting Detection")

# GUI Components
tk.Label(root, text="Enter Tape Input:").pack()
entry = tk.Entry(root, width=30)
entry.pack()

selected_example = StringVar(root)
selected_example.set("Flip 0 to 1")
tk.Label(root, text="Select TM Example:").pack()
OptionMenu(root, selected_example, *tm_examples.keys()).pack()

tk.Button(root, text="Simulate TM", command=simulate_tm_gui).pack(pady=5)

output_area = scrolledtext.ScrolledText(root, width=70, height=8, wrap=tk.WORD)
output_area.pack(padx=10, pady=5)

transition_area = scrolledtext.ScrolledText(root, width=70, height=6, wrap=tk.WORD)
transition_area.pack(padx=10, pady=5)

verdict_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
verdict_label.pack(pady=5)

tape_canvas = tk.Canvas(root, width=700, height=70, bg="lightgray")
tape_canvas.pack(pady=10)

root.mainloop()