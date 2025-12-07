from sudoku import Sudoku
from solver import CspSolver
from generator import generate
import time

print("=== 9×9 Sudoku CSP Solver ===\n")

while True:
    choice = input("Generate random sudoku? (y/n): ").strip().lower()
    if choice in ("y", "n"):
        break
    print("Enter only 'y' or 'n'.")

if choice == "y":
    print("\nSelect difficulty:")
    print("  1 - Easy (40% empty)")
    print("  2 - Medium (55% empty)")
    print("  3 - Hard (70% empty)")

    while True:
        level = input("Enter choice (1-3): ").strip()
        if level in ("1", "2", "3"):
            break
        print("Enter only 1, 2 or 3!")

    if level == "1":
        sudoku = generate(int(0.40 * 81))
        diff_name = "Easy"
    elif level == "2":
        sudoku = generate(int(0.55 * 81))
        diff_name = "Medium"
    else:
        sudoku = generate(int(0.70 * 81))
        diff_name = "Hard"

    print(f"\nGenerated {diff_name} sudoku!\n")

else:
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

sdk = Sudoku(sudoku)

print("Initial sudoku:")
sdk.print()

use_mrv = input("Enable MRV? (y/n): ").strip().lower() == "y"
use_degree = input("Enable Degree heuristic? (y/n): ").strip().lower() == "y"
use_lcv = input("Enable LCV? (y/n): ").strip().lower() == "y"

print(f"\nSolving with: MRV={use_mrv}, Degree={use_degree}, LCV={use_lcv}")

solver = CspSolver(sdk, mrv=use_mrv, degree=use_degree, lcv=use_lcv)

start = time.time()
solved = solver.solve()
end = time.time()

print(f"\nTime elapsed: {round((end - start)*1000, 2)} ms")

if solved:
    print("\nSolution found:")
    sdk.print()
else:
    print("\nNo solution exists.")

print("\nBacktracks:", solver.backtracks)
input("\nPress Enter to exit...")
