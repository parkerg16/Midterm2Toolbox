import sys
from colorama import init, Fore, Style
from tabulate import tabulate


def create_shift_table(pattern):
    """
    Creates the shift table for Horspool's algorithm.
    """
    shift_table = {}
    m = len(pattern)
    for i in range(m - 1):
        shift_table[pattern[i]] = m - 1 - i
    return shift_table


def horspool_search(text, pattern):
    """
    Performs Horspool's algorithm with specified output format.
    """
    init(autoreset=True)

    if isinstance(text, str):
        text = list(text)
    if isinstance(pattern, str):
        pattern = list(pattern)

    shift_table = create_shift_table(pattern)
    m = len(pattern)
    n = len(text)
    positions = []
    steps = []
    step_count = 1
    i = 0

    while i <= n - m:
        current_window = ''.join(text[i:i + m])
        k = m - 1
        match = True

        while k >= 0 and i + k < n:
            if pattern[k] != text[i + k]:
                match = False
                break
            k -= 1

        if match and k < 0:
            steps.append(f"Step {step_count}: The solution has been found at index {i}")
            positions.append(i)
            break
        else:
            mismatched_char = text[i + m - 1]
            shift = shift_table.get(mismatched_char, m)
            steps.append(f"Step {step_count}: {mismatched_char}: {current_window} Shift {shift}")
            i += shift
            step_count += 1

    if not positions:
        steps.append(f"Step {step_count}: Pattern not found in the text")

    return steps, positions


def main():
    init(autoreset=True)

    # Example usage
    text = "GTACTAGAGGACGTATGTACTG"
    pattern = "ATGTA"

    steps, positions = horspool_search(text, pattern)

    # Print steps
    for step in steps:
        print(step)


if __name__ == "__main__":
    main()