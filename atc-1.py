import tkinter as tk
from tkinter import scrolledtext

class TuringMachine:
    def __init__(self, states, tape_alphabet, start_state, accept_state, transitions, input_string):
        self.states = states
        self.tape_alphabet = tape_alphabet
        self.start_state = start_state
        self.accept_state = accept_state
        self.transitions = transitions

        self.tape = list(input_string) + ['_'] * 100
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

    def run(self, max_steps=1000):
        log = []
        while self.steps < max_steps:
            log.append(f"Step {self.steps}: State={self.current_state}, Head={self.head}, Tape={''.join(self.tape).strip('_')}")
            cont, message = self.step()
            if not cont or self.current_state == self.accept_state:
                log.append(message)
                break
        return log


# Example TM: changes 0 to 1 and halts
tm_def = {
    "states": ["q0", "q1", "halt"],
    "tape_alphabet": ["0", "1", "_"],
    "start_state": "q0",
    "accept_state": "halt",
    "transitions": {
        "q0_0": ["q1", "1", "R"],
        "q1__": ["halt", "_", "N"]
    }
}

# GUI Setup
def simulate_tm():
    tape_input = entry.get()
    tm = TuringMachine(
        states=tm_def["states"],
        tape_alphabet=tm_def["tape_alphabet"],
        start_state=tm_def["start_state"],
        accept_state=tm_def["accept_state"],
        transitions=tm_def["transitions"],
        input_string=tape_input
    )
    result = tm.run()
    output_area.delete("1.0", tk.END)
    for line in result:
        output_area.insert(tk.END, line + "\n")

root = tk.Tk()
root.title("Turing Machine Simulator")

tk.Label(root, text="Enter Tape Input:").pack()
entry = tk.Entry(root, width=30)
entry.pack()

tk.Button(root, text="Simulate TM", command=simulate_tm).pack(pady=5)

output_area = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
output_area.pack(padx=10, pady=10)

root.mainloop()
