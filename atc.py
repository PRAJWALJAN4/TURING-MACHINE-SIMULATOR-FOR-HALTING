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
            print(f"No transition for ({self.current_state}, {symbol}) — halting.")
            return False

        next_state, write_symbol, direction = self.transitions[key]
        self.tape[self.head] = write_symbol
        self.current_state = next_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

        self.steps += 1
        return self.current_state != self.accept_state

    def run(self, max_steps=1000, verbose=True):
        while self.steps < max_steps:
            if verbose:
                tape_str = ''.join(self.tape).strip('_')
                print(f"Step {self.steps}: State={self.current_state}, Head={self.head}, Tape={tape_str}")
            if not self.step():
                break
        return self.current_state == self.accept_state


# ========== Hardcoded Example TM ==========
example_tm = {
    "states": ["q0", "q1", "halt"],
    "tape_alphabet": ["0", "1", "_"],
    "start_state": "q0",
    "accept_state": "halt",
    "transitions": {
        "q0_0": ["q1", "1", "R"],
        "q1__": ["halt", "_", "N"]
    }
}

# ========== Halting Checker Simulation ==========
def halts(tm_func, input_str):
    try:
        tm = tm_func(input_str)
        return tm.run(verbose=False)
    except RecursionError:
        print("RecursionError: possible undecidable behavior.")
        return False


# ========== Self-referential Pathological TM ==========
def paradox_tm(input_str):
    def mock_halting_machine(s):
        return halts(paradox_tm, s)

    if mock_halting_machine(input_str):
        while True:
            pass  # Loop forever if halts returns True
    else:
        return TuringMachine(
            states=["start", "halt"],
            tape_alphabet=["0", "1", "_"],
            start_state="start",
            accept_state="halt",
            transitions={
                "start_0": ["halt", "0", "N"]
            },
            input_string=input_str
        )


# ========== Main Execution ==========
if __name__ == '__main__':
    print("=== Basic Turing Machine Simulation ===")
    user_input = input("Enter tape input (e.g., 0): ").strip()
    tm = TuringMachine(
        states=example_tm["states"],
        tape_alphabet=example_tm["tape_alphabet"],
        start_state=example_tm["start_state"],
        accept_state=example_tm["accept_state"],
        transitions=example_tm["transitions"],
        input_string=user_input
    )
    halted = tm.run()
    print("\nResult:", "Halted Successfully" if halted else "Did Not Halt")

    print("\n=== Halting Problem Demo ===")
    print("Simulating a self-referential TM... This may loop or crash (simulated undecidability).")
    try:
        halts(paradox_tm, "0")
    except Exception as e:
        print(f"Simulation failed due to: {e}")
