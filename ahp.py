import numpy as np
import pandas as pd

# Pairwise comparison matrix (criteria for overall items)
criteria = [
    [1, 5, 7, 7, 7, 3, 8],
    [0.2, 1, 3, 3, 3, 0.33, 4],
    [0.14, 0.33, 1, 1, 1, 0.2, 2],
    [0.14, 0.33, 1, 1, 1, 0.2, 2],
    [0.14, 0.33, 1, 1, 1, 0.2, 2],
    [0.33, 3, 5, 5, 5, 1, 6],
    [0.125, 0.25, 0.5, 0.5, 0.5, 0.17, 1]
]

# Labels for criteria items
criteria_labels = [
    "Security Camera", "Smart Doorbell", "Smart Lights", "Outlets",
    "Thermostat", "Mobile App Access", "Voice Assistant Integration"
]


# Function to calculate priority vector and format outputs for Excel
def calculate_ahp(matrix, labels):
    matrix = np.array(matrix)
    column_sums = matrix.sum(axis=0)
    normalized_matrix = matrix / column_sums
    priority_vector = normalized_matrix.mean(axis=1)

    # Prepare DataFrames for Excel output
    pairwise_df = pd.DataFrame(matrix, index=labels, columns=labels)
    column_sums_df = pd.DataFrame([column_sums], columns=labels, index=["Column Sums"])
    normalized_df = pd.DataFrame(normalized_matrix, index=labels, columns=labels)
    priority_vector_df = pd.DataFrame({
        "Item": labels,
        "Weight": priority_vector
    })

    # Display all outputs
    print("\nPairwise Comparison Matrix:\n", pairwise_df)
    print("\nColumn Sums:\n", column_sums_df)
    print("\nNormalized Matrix:\n", np.round(normalized_df, 4))
    print("\nPriority Vector (Weights):")
    for i, weight in enumerate(priority_vector):
        print(f"{labels[i]}: {weight:.4f}")

    # Console-friendly Excel outputs for each section
    pairwise_excel_str = pairwise_df.to_csv(sep='\t', index=True)
    column_sums_excel_str = column_sums_df.to_csv(sep='\t', index=True)
    normalized_excel_str = normalized_df.to_csv(sep='\t', index=True)
    priority_vector_excel_str = priority_vector_df.to_csv(sep='\t', index=False)

    print("\nExcel Friendly Output - Pairwise Comparison Matrix:\n")
    print(pairwise_excel_str)
    print("\nExcel Friendly Output - Column Sums:\n")
    print(column_sums_excel_str)
    print("\nExcel Friendly Output - Normalized Matrix:\n")
    print(normalized_excel_str)
    print("\nExcel Friendly Output - Priority Vector:\n")
    print(priority_vector_excel_str)

    return pairwise_df, column_sums_df, normalized_df, priority_vector_df


# Calculate priority vector for the criteria matrix
print("Criteria Matrix (Overall Requirements):")
criteria_pairwise_df, criteria_column_sums_df, criteria_normalized_df, criteria_priority_vector_df = calculate_ahp(
    criteria, criteria_labels)

# Functional Requirements (FR) Matrix
fr_matrix = [
    [1, 3, 3, 7, 7, 5, 5, 5],  # Live video feed access
    [0.33, 1, 1, 5, 5, 3, 3, 3],  # Motion detection alerts
    [0.33, 1, 1, 5, 5, 3, 3, 3],  # Video recording and storage
    [0.14, 0.2, 0.2, 1, 1, 0.33, 0.33, 0.33],  # Video intercom functionality
    [0.14, 0.2, 0.2, 1, 1, 0.33, 0.33, 0.33],  # Remote answering capability
    [0.2, 0.33, 0.33, 3, 3, 1, 1, 1],  # Remote control capabilities
    [0.2, 0.33, 0.33, 3, 3, 1, 1, 1],  # Scheduling functionality
    [0.2, 0.33, 0.33, 3, 3, 1, 1, 1],  # Integration with motion sensors
]

# Labels for FR items
fr_labels = [
    "Live video feed access",
    "Motion detection alerts",
    "Video recording and storage",
    "Video intercom functionality",
    "Remote answering capability",
    "Remote control capabilities",
    "Scheduling functionality",
    "Integration with motion sensors"
]

print("\nFunctional Requirements (FR) Matrix:")
fr_pairwise_df, fr_column_sums_df, fr_normalized_df, fr_priority_vector_df = calculate_ahp(fr_matrix, fr_labels)

# Non-Functional Requirements (NFR) Matrix
nfr_matrix = [
    [1, 5, 7, 3, 8],  # High-quality video streaming
    [0.2, 1, 3, 0.33, 4],  # Reliable connectivity
    [0.14, 0.33, 1, 0.2, 2],  # Quick response time
    [0.33, 3, 5, 1, 6],  # App response time under 3 seconds
    [0.125, 0.25, 0.5, 0.17, 1],  # 99.9% app uptime and reliability
]

# Labels for NFR items
nfr_labels = [
    "High-quality video streaming",
    "Reliable connectivity",
    "Quick response time",
    "App response time under 3 seconds",
    "99.9% app uptime and reliability"
]

print("\nNon-Functional Requirements (NFR) Matrix:")
nfr_pairwise_df, nfr_column_sums_df, nfr_normalized_df, nfr_priority_vector_df = calculate_ahp(nfr_matrix, nfr_labels)
