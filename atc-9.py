import tkinter as tk
from tkinter import scrolledtext, StringVar, OptionMenu
import networkx as nx
import matplotlib.pyplot as plt

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

        if self.head >= len(self.tape):
            self.tape.append('_')
        if self.head < 0:
            self.tape.insert(0, '_')
            self.head = 0

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

# TM Definitions
tm_examples = {
    "Match 0ⁿ1ⁿ (e.g. 000111)": {
        "states": ["q0", "q1", "q2", "q3", "halt", "reject"],
        "tape_alphabet": ["0", "1", "X", "Y", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            "q0_0": ["q1", "X", "R"],
            "q0_Y": ["q0", "Y", "R"],
            "q0__": ["halt", "_", "N"],
            "q1_0": ["q1", "0", "R"],
            "q1_Y": ["q1", "Y", "R"],
            "q1_1": ["q2", "Y", "L"],
            "q2_0": ["q2", "0", "L"],
            "q2_X": ["q0", "X", "R"],
            "q2_Y": ["q2", "Y", "L"],
            "q1__": ["reject", "_", "N"],
            "q0_1": ["reject", "1", "N"]
        }
    },
    "Unary Increment (e.g. 111 → 1111)": {
        "states": ["q0", "halt"],
        "tape_alphabet": ["1", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "reject_state": "halt",
        "transitions": {
            "q0_1": ["q0", "1", "R"],
            "q0__": ["halt", "1", "N"]
        }
    },
    "Even number of 1s": {
        "states": ["even", "odd", "halt", "reject"],
        "tape_alphabet": ["1", "_"],
        "start_state": "even",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            "even_1": ["odd", "1", "R"],
            "odd_1": ["even", "1", "R"],
            "even__": ["halt", "_", "N"],
            "odd__": ["reject", "_", "N"]
        }
    },
    "Binary Palindrome Checker (e.g. 10101)": {
        "states": ["q0", "q1", "q2", "q3", "q4", "q5", "halt", "reject"],
        "tape_alphabet": ["0", "1", "X", "_"],
        "start_state": "q0",
        "accept_state": "halt",
        "reject_state": "reject",
        "transitions": {
            "q0_0": ["q1", "X", "R"],
            "q0_1": ["q2", "X", "R"],
            "q0_X": ["halt", "X", "N"],
            "q0__": ["halt", "_", "N"],
            "q1_0": ["q1", "0", "R"],
            "q1_1": ["q1", "1", "R"],
            "q1_X": ["q1", "X", "R"],
            "q1__": ["q3", "_", "L"],
            "q2_0": ["q2", "0", "R"],
            "q2_1": ["q2", "1", "R"],
            "q2_X": ["q2", "X", "R"],
            "q2__": ["q4", "_", "L"],
            "q3_0": ["q5", "X", "L"],
            "q4_1": ["q5", "X", "L"],
            "q3_X": ["halt", "X", "N"],
            "q4_X": ["halt", "X", "N"],
            "q5_0": ["q5", "0", "L"],
            "q5_1": ["q5", "1", "L"],
            "q5_X": ["q0", "X", "R"]
        }
    }
}

# Automaton Definitions (for DFA/NFA Viewer)
automaton_definitions = {
    "Match 0ⁿ1ⁿ (e.g. 000111)": {
        "type": "NFA",
        "states": ["q0", "q1", "q2", "halt", "reject"],
        "transitions": {
            "q0": {"0": ["q1"], "1": ["reject"]},
            "q1": {"1": ["q2"]},
            "q2": {"_": ["halt"]}
        },
        "start": "q0",
        "accept": ["halt"]
    },
    "Unary Increment (e.g. 111 → 1111)": {
        "type": "DFA",
        "states": ["q0", "halt"],
        "transitions": {
            "q0": {"1": "q0", "_": "halt"}
        },
        "start": "q0",
        "accept": ["halt"]
    },
    "Even number of 1s": {
        "type": "DFA",
        "states": ["even", "odd", "halt", "reject"],
        "transitions": {
            "even": {"1": "odd", "_": "halt"},
            "odd": {"1": "even", "_": "reject"}
        },
        "start": "even",
        "accept": ["halt"]
    },
    "Binary Palindrome Checker (e.g. 10101)": {
        "type": "NFA",
        "states": ["q0", "q1", "q2", "q3", "halt"],
        "transitions": {
            "q0": {"0": ["q1"], "1": ["q2"], "_": ["halt"]},
            "q1": {"0": ["q1"], "_": ["q3"]},
            "q2": {"1": ["q2"], "_": ["q3"]},
            "q3": {"0": ["halt"], "1": ["halt"]}
        },
        "start": "q0",
        "accept": ["halt"]
    }
}

# GUI Logic
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
        transition_area.insert(tk.END, tm.transition_trace[-1] + "\n")
        update_tape(tm)
        if cont and not tm.halted:
            root.after(150, run_tm_step)
        else:
            verdict = "✅ Accepted" if tm.is_accepted() else "❌ Rejected" if tm.is_rejected() else "⚠️ Halted"
            verdict_label.config(text=verdict)
            open_automaton_gui()

def update_tape(tm):
    tape_canvas.delete("all")
    x_start = 10
    cell_size = 30
    for i in range(tm.head - 10, tm.head + 11):
        symbol = "_" if i < 0 or i >= len(tm.tape) else tm.tape[i]
        x = x_start + (i - tm.head + 10) * cell_size
        tape_canvas.create_rectangle(x, 10, x + cell_size, 40,
                                     fill="yellow" if i == tm.head else "white", outline="black")
        tape_canvas.create_text(x + cell_size / 2, 25, text=symbol)
        if i == tm.head:
            tape_canvas.create_text(x + cell_size / 2, 55, text=tm.current_state, font=("Arial", 8, "italic"))

def open_automaton_gui():
    selected = selected_example.get()
    auto = automaton_definitions[selected]
    G = nx.MultiDiGraph()
    label = auto["type"]

    for state in auto["states"]:
        G.add_node(state)

    for src, trans in auto["transitions"].items():
        for sym, dst in trans.items():
            if isinstance(dst, list):
                for d in dst:
                    G.add_edge(src, d, label=sym)
            else:
                G.add_edge(src, dst, label=sym)

    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}

    win = tk.Toplevel(root)
    win.title(f"{label} Representation")
    tk.Label(win, text=f"{label} — State Transition Diagram", font=("Arial", 14, "bold")).pack(pady=5)

    fig = plt.figure(figsize=(5, 4))
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.tight_layout()
    fig.savefig("automaton_graph.png")

    canvas = tk.Canvas(win, width=500, height=400)
    canvas.pack()
    img = tk.PhotoImage(file="automaton_graph.png")
    canvas.create_image(250, 200, image=img)
    canvas.image = img

# GUI Setup
root = tk.Tk()
root.title("Turing Machine Simulator — DFA/NFA Viewer")

tk.Label(root, text="Enter Input String:").pack()
entry = tk.Entry(root, width=30)
entry.pack()

selected_example = StringVar(root)
selected_example.set(list(tm_examples.keys())[0])
tk.Label(root, text="Select TM Language:").pack()
OptionMenu(root, selected_example, *tm_examples.keys()).pack()

tk.Button(root, text="Run Simulation", command=simulate_tm_gui).pack(pady=5)

output_area = scrolledtext.ScrolledText(root, width=70, height=8, wrap=tk.WORD)
output_area.pack(padx=10, pady=5)

tk.Label(root, text="Transitions:").pack()
transition_area = scrolledtext.ScrolledText(root, width=70, height=6, wrap=tk.WORD)
transition_area.pack(padx=10, pady=5)

verdict_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
verdict_label.pack(pady=5)

tape_canvas = tk.Canvas(root, width=700, height=70, bg="lightgray")
tape_canvas.pack(pady=10)

root.mainloop()
