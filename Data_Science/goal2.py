import math
import matplotlib.pyplot as plt
import numpy as np

threshold = 0.05
batch_size = 1000


def check_type(pdg_code):
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    return 0

def poisson_distribution(average):
    return math.sqrt(average)

def difference(no_1, no_2):
    return abs(no_1 - no_2)

def combined_uncertainty(no_1, no_2):
    return math.sqrt(poisson_distribution(no_1)**2 + poisson_distribution(no_2)**2)

def significance(no_1, no_2, comb_uncertainty):
    if comb_uncertainty == 0:
        return float('inf')
    return difference(no_1, no_2) / comb_uncertainty


def read_events(filename):
    try:
        with open(filename, "r") as f:
            while True:
                header = f.readline()
                if not header:
                    break
                parts = header.strip().split()
                if len(parts) != 2:
                    continue  # linie invalidă
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
        print("File not found. Please check the file path.")
        exit()
    except IOError:
        print("Error reading the file. Please check the file permissions.")
        exit()


total_pos = 0
total_neg = 0
event_count = 0
batch_pos = []
batch_neg = []

current_batch_pos = 0
current_batch_neg = 0

for event_id, particles in read_events("_Data/output-Set1.txt"):
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


average_pos = total_pos / event_count
average_neg = total_neg / event_count
poisson_pos = poisson_distribution(total_pos)
poisson_neg = poisson_distribution(total_neg)
diff = difference(total_pos, total_neg)
comb_unc = combined_uncertainty(total_pos, total_neg)
sig = significance(total_pos, total_neg, comb_unc)


print(f"In {event_count} total events, we had {total_pos} positive particles and {total_neg} negative particles.")
print(f"There’s an average of {average_pos:.10f} particles (positive pions) per event.")
print(f"There’s an average of {average_neg:.10f} antiparticles (negative pions) per event.")
print(f"The Poisson distribution for the positive pions is {poisson_pos:.10f}")
print(f"The Poisson distribution for the negative (antiparticle) pions is {poisson_neg:.10f}")
print(f"There are {diff} more particles than antiparticles.")
print(f"The combined uncertainty of the total number of particles and antiparticles is {comb_unc:.10f}")
print(f"The significance of the difference is {sig:.10f}")
print(f"Difference between positive and negative pions: {diff:.10f}")
if sig > threshold:
    print("The significance is very large compared to the threshold.")
else:
    print("The significance is not large compared to the threshold.")


x_vals = np.arange(0, len(batch_pos)) * batch_size
plt.plot(x_vals, batch_pos, label="Positive Pions", color="blue")
plt.plot(x_vals, batch_neg, label="Negative Pions", color="red")
plt.xlabel("Event number")
plt.ylabel("Number of pions in 1000 events")
plt.title("Positive and Negative Pions per 1000 Events")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Data_Science/table.png")