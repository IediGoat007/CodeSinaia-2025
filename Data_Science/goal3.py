import math
import time
import os

# Calculates average and statistical uncertainty
def calculate_average_and_uncertainty(total, count):
    if count == 0:
        return 0, 0
    average = total / count
    uncertainty = math.sqrt(total) / count if total > 0 else 0
    return average, uncertainty

# Determines particle type based on PDG code (1 for positive pion, -1 for negative pion, 0 otherwise)
def check_type(pdg_code):
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    return 0

# TODO: Set batch_size (e.g., 1000) to control memory usage.
# TODO: Prepare a list of file paths to process.

# TODO: For each file:
#       - Open the file and read event and particle data.
#       - For each event, count positive and negative pions using check_type.
#       - Use batching (e.g., sum per 1000 events) to aggregate results for memory efficiency.
#       - After each batch, add batch results to the totals and reset batch counters.
#       - After all events, add any remaining batch counts to the totals.

# TODO: After processing each file:
#       - Calculate averages and uncertainties for positive and negative pions per event.
#       - Calculate the mean difference, combined uncertainty, and significance (in sigma).
#       - Print the results, including whether the difference is statistically significant.

# TODO: Print the overall execution time at the end.

# Expected output:
# - For each file: averages, uncertainties, mean difference, combined uncertainty, significance, and a statement about statistical significance.
# - At the end: total execution time.

# Note: Batching is used here for memory efficiency, but sampling (storing per-event counts) could also be used if per-event analysis or plotting is needed.

def read_events(filename):
    try:
        with open(filename, "r") as f:
            while True:
                header = f.readline()
                if not header:
                    break
                parts = header.strip().split()
                if len(parts) != 2:
                    continue
                event_id = int(parts[0])
                num_particles = int(parts[1])
                particles = []
                for _ in range(num_particles):
                    line = f.readline()
                    if not line:
                        break
                    particles.append(line.strip())
                yield event_id, particles
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return
    except IOError:
        print(f"Error reading file: {filename}")
        return

def combined_uncertainty(no_1, no_2):
    return math.sqrt((math.sqrt(no_1) if no_1 > 0 else 0) ** 2 + (math.sqrt(no_2) if no_2 > 0 else 0) ** 2)

def significance(no_1, no_2, comb_uncertainty):
    if comb_uncertainty == 0:
        return float('inf')
    return abs(no_1 - no_2) / comb_uncertainty

def process_file(filepath, batch_size=1000, threshold=0.05):
    total_pos = 0
    total_neg = 0
    event_count = 0
    current_batch_pos = 0
    current_batch_neg = 0
    batch_pos = []
    batch_neg = []
    for event_id, particles in read_events(filepath):
        pos_count = 0
        neg_count = 0
        for p_line in particles:
            parts = p_line.split()
            if len(parts) < 4:
                continue
            try:
                pdg_code = int(parts[3])
            except ValueError:
                continue
            type_flag = check_type(pdg_code)
            if type_flag == 1:
                pos_count += 1
            elif type_flag == -1:
                neg_count += 1
        total_pos += pos_count
        total_neg += neg_count
        current_batch_pos += pos_count
        current_batch_neg += neg_count
        event_count += 1
        if event_count % batch_size == 0:
            batch_pos.append(current_batch_pos)
            batch_neg.append(current_batch_neg)
            current_batch_pos = 0
            current_batch_neg = 0
    # Add any remaining batch
    if current_batch_pos > 0 or current_batch_neg > 0:
        batch_pos.append(current_batch_pos)
        batch_neg.append(current_batch_neg)
    avg_pos, unc_pos = calculate_average_and_uncertainty(total_pos, event_count)
    avg_neg, unc_neg = calculate_average_and_uncertainty(total_neg, event_count)
    diff = abs(total_pos - total_neg)
    comb_unc = combined_uncertainty(total_pos, total_neg)
    sig = significance(total_pos, total_neg, comb_unc)
    print(f"\nFile: {os.path.basename(filepath)}")
    print(f"  Events: {event_count}")
    print(f"  Positive pions: {total_pos}, Negative pions: {total_neg}")
    print(f"  Average positive pions/event: {avg_pos:.10f} ± {unc_pos:.10f}")
    print(f"  Average negative pions/event: {avg_neg:.10f} ± {unc_neg:.10f}")
    print(f"  Difference: {diff}")
    print(f"  Combined uncertainty: {comb_unc:.10f}")
    print(f"  Significance: {sig:.10f}")
    if sig > threshold:
        print("  The significance is very large compared to the threshold.")
    else:
        print("  The significance is not large compared to the threshold.")

def main():
    start_time = time.time()
    data_dir = os.path.join(os.path.dirname(__file__), "..", "_Data")
    files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.startswith("output-Set") and f.endswith(".txt")]
    files.sort()
    if not files:
        print("No data files found.")
        return
    for filepath in files:
        process_file(filepath)
    elapsed = time.time() - start_time
    print(f"\nTotal execution time: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()