import tkinter as tk
from tkinter import scrolledtext, StringVar, OptionMenu

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
        self.transition_trace = []

    def step(self):
        symbol = self.tape[self.head]
        key = f"{self.current_state}_{symbol}"

        if key not in self.transitions:
            return False, f"No transition for ({self.current_state}, {symbol}) — halting."

        next_state, write_symbol, direction = self.transitions[key]
        self.transition_trace.append(f"({self.current_state}, {symbol}) → ({next_state}, {write_symbol}, {direction})")

        self.tape[self.head] = write_symbol
        self.current_state = next_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

        self.steps += 1
        return True, f"Step {self.steps}: State={self.current_state}, Head={self.head}, Tape={''.join(self.tape).strip('_')}"

    def is_accepted(self):
        return self.current_state == self.accept_state


# TM Definitions
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
    "Halting Problem": {
        "states": ["loop"],
        "tape_alphabet": ["0", "1", "_"],
        "start_state": "loop",
        "accept_state": "halt",
        "transitions": {
            "loop_0": ["loop", "0", "R"],
            "loop__": ["loop", "_", "R"]
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
        transitions=tm_def["transitions"],
        input_string=entry.get()
    )
    output_area.delete("1.0", tk.END)
    transition_area.delete("1.0", tk.END)
    verdict_label.config(text="")
    update_tape(tm)
    root.after(500, run_tm_step)


def run_tm_step():
    cont, msg = tm.step()
    output_area.insert(tk.END, msg + "\n")
    update_tape(tm)

    if cont and not tm.is_accepted():
        root.after(500, run_tm_step)
    else:
        transition_area.insert(tk.END, "\n".join(tm.transition_trace))
        verdict = "✅ Input is accepted by the Turing Machine." if tm.is_accepted() else "❌ Input is rejected."
        verdict_label.config(text=verdict)


def update_tape(tm):
    tape_canvas.delete("all")
    x_start = 10
    cell_size = 30

    for i in range(tm.head - 10, tm.head + 11):
        symbol = tm.tape[i] if 0 <= i < len(tm.tape) else "_"
        x = x_start + (i - tm.head + 10) * cell_size
        tape_canvas.create_rectangle(x, 10, x + cell_size, 40, fill="yellow" if i == tm.head else "white", outline="black")
        tape_canvas.create_text(x + cell_size / 2, 25, text=symbol)

        # Display state below the tape
        state_text = tm.current_state if i == tm.head else ""
        tape_canvas.create_text(x + cell_size / 2, 55, text=state_text, font=("Arial", 8, "italic"))


# Main Window Setup
root = tk.Tk()
root.title("Turing Machine Visual Simulator")

# Input & Example Selection
tk.Label(root, text="Enter Tape Input:").pack()
entry = tk.Entry(root, width=30)
entry.pack()

selected_example = StringVar(root)
selected_example.set("Flip 0 to 1")
tk.Label(root, text="Select TM Example:").pack()
OptionMenu(root, selected_example, *tm_examples.keys()).pack()

# Simulate Button
tk.Button(root, text="Simulate TM", command=simulate_tm_gui).pack(pady=5)

# Output Areas
output_area = scrolledtext.ScrolledText(root, width=70, height=8, wrap=tk.WORD)
output_area.pack(padx=10, pady=5)

transition_area = scrolledtext.ScrolledText(root, width=70, height=6, wrap=tk.WORD)
transition_area.pack(padx=10, pady=5)

verdict_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
verdict_label.pack(pady=5)

tape_canvas = tk.Canvas(root, width=700, height=70, bg="lightgray")
tape_canvas.pack(pady=10)

root.mainloop()
