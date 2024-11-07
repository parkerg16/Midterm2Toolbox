def does_something(A, x, y):
    """
    Input:
    - A: List of integers between x and y (inclusive)
    - x: Minimum integer value in A
    - y: Maximum integer value in A

    Returns:
    - C: Sorted list of integers
    """
    n = len(A)
    k = y - x + 1  # Range of input integers

    # Step 1: Initialize B[0..k-1] to 0
    B = [0] * k

    # Step 2: Count the occurrences of each integer
    for i in range(n):
        B[A[i] - x] += 1

    # Step 3: Compute the cumulative counts
    for j in range(1, k):
        B[j] = B[j - 1] + B[j]

    # Step 4: Place the elements into the output array C
    C = [0] * n
    for i in range(n - 1, -1, -1):
        j = A[i] - x
        C[B[j] - 1] = A[i]
        B[j] -= 1

    return C


# Example usage
if __name__ == "__main__":
    A = [6, 0, 2, 0, 1, 3, 4, 6, 1, 3, 2]
    x = min(A)
    y = max(A)
    sorted_A = does_something(A, x, y)
    print("Original array:", A)
    print("Sorted array:", sorted_A)
