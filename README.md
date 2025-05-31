# turing-machine-simulator-for-hallting
# 🧠 Turing Machine Simulator with DFA/NFA Visualizer

This is an interactive **Turing Machine Simulator** with built-in **DFA/NFA visualizer**, built using Python and Tkinter. It simulates the behavior of basic Turing Machines and displays live transitions, tape updates, and final results. After each simulation, it also opens a graphical representation of the DFA or NFA structure relevant to the language.vvf

---

## 🚀 Features

- ✅ Simulate Turing Machines step-by-step.
- 🎥 Live transition trace and tape movement.
- 🧾 Verdict display (Accepted / Rejected / Halted).
- 📈 Automatic DFA/NFA GUI after simulation.
- 🧠 Multiple predefined TM examples:
  - Match `0ⁿ1ⁿ` (e.g., `000111`)
  - Unary increment (e.g., `111` → `1111`)
  - Even number of `1`s
  - Binary palindrome checker (e.g., `10101`)

---

## 🛠️ Requirements

Install required packages using:

```bash
pip install networkx matplotlib
