import math
import time
import random
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

# === Funcții de bază ===
def calculate_average_and_uncertainty(total, count):
    if count == 0:
        return 0, 0
    average = total / count
    uncertainty = math.sqrt(total) / count
    return average, uncertainty

def check_type(pdg_code):
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    return 0

def read_events(filename, subsample_size=None, batch_size=1000):
    try:
        with open(filename, "r") as f:
            batch = []
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

                batch.append((event_id, particles))

                if len(batch) == batch_size:
                    yield batch
                    batch = []

            if batch:
                yield batch

    except FileNotFoundError:
        print(f"[ERROR] File not found: {filename}")
    except IOError:
        print(f"[ERROR] Error reading file: {filename}")

def process_file(args):
    file_index, path = args
    total_pos = 0
    total_neg = 0
    event_count = 0
    batch_pos_list = []
    batch_neg_list = []
    results = []
    for batch in read_events(path, batch_size=1000):
        current_batch_pos = 0
        current_batch_neg = 0
        for event_id, particles in batch:
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
        batch_pos_list.append(current_batch_pos)
        batch_neg_list.append(current_batch_neg)
    avg_pos, unc_pos = calculate_average_and_uncertainty(total_pos, event_count)
    avg_neg, unc_neg = calculate_average_and_uncertainty(total_neg, event_count)
    mean_diff = avg_pos - avg_neg
    combined_unc = math.sqrt(unc_pos**2 + unc_neg**2)
    significance = mean_diff / combined_unc if combined_unc != 0 else 0
    return {
        'file_index': file_index,
        'path': path,
        'avg_pos': avg_pos,
        'unc_pos': unc_pos,
        'avg_neg': avg_neg,
        'unc_neg': unc_neg,
        'mean_diff': mean_diff,
        'combined_unc': combined_unc,
        'significance': significance
    }

# === Procesare fișiere ===
file_paths = [f"_Data/output-Set{i}.txt" for i in range(1, 11)]

start_time = time.time()

with ProcessPoolExecutor() as executor:
    futures = [executor.submit(process_file, (file_index, path)) for file_index, path in enumerate(file_paths, start=1)]
    results = []
    for future in as_completed(futures):
        result = future.result()
        results.append(result)

# Sort results by file_index to maintain order
results.sort(key=lambda x: x['file_index'])

for result in results:
    print(f"\n[INFO] Processing file {result['file_index']}: {result['path']}")
    print(f"[RESULT] File: {result['path']}")
    print(f"  Average positive pions/event: {result['avg_pos']:.4f} ± {result['unc_pos']:.4f}")
    print(f"  Average negative pions/event: {result['avg_neg']:.4f} ± {result['unc_neg']:.4f}")
    print(f"  Mean difference: {result['mean_diff']:.4f}")
    print(f"  Combined uncertainty: {result['combined_unc']:.4f}")
    print(f"  Significance (σ): {result['significance']:.2f}")
    if abs(result['significance']) >= 2:
        print("  → Statistically significant difference.")
    else:
        print("  → No statistically significant difference.")

end_time = time.time()
print(f"\n[INFO] Total execution time: {end_time - start_time:.2f} seconds")