import math

def calculate_p(px, py, pz):    #This function calculates the momentum of a particle given its components.
    p = math.sqrt(px**2 + py**2 + pz**2)  #uses the formula for P
    return p       

def calculate_pT (px, py):    #This function calculates the transverse momentum of a particle given its x and y components.    
    pt = math.sqrt(px**2 + py**2)       #uses the formula for Pt
    return pt

def calculate_pseudorapidity(p, pz):               #pseudorapidity is the n with a long end
    ps = 0.5 * (math.log((p + pz) / (p - pz)))  #uses the formula for pseudorapidity
    return ps       

def calculate_azimuthal_angle(px, py):      #solve if you finish early
    phi = math.atan(px/py)  #uses the formula for azimuthal angle
    return phi          

def check_type (pdg_code):      #this function checks the type of particle based on the pdg code
    if pdg_code == 211:
        print("pion+")
    elif pdg_code == -211:
        print("pion-")
    elif pdg_code == 111:
        print("pion0")
    else:
        print("not a pion")



#       Open the input file, read the first line to get event_id and num_particles,
#       then read the rest of the lines into lines_list as lists of strings.
try:
    with open("_Data/output-Set0.txt", "r") as infile:  #open the file in read mode
        first_line = infile.readline().strip()  #read the first line and remove any leading/trailing whitespace
        event_id, num_particles = map(int, first_line.split())  #split the line into event_id and num_particles
        lines_list = [line.strip().split() for line in infile]  #read the rest of the lines into a list of lists

except FileNotFoundError:
    print("File not found. Please check the file path.")
except IOError:
    print("Error reading the file. Please check the file format.")

print("event id is", event_id, "and there are", num_particles, "particles")       #print to show the events id and no of particles in the event


#       Loop through each particle in lines_list, convert values to float,
#       call the analysis/calculation functions, and print the results as shown.
for i in range(len(lines_list)):
    print()
    print ("Particle", i + 1)  #print the particle number
    px, py, pz, pdg_code = map(float, lines_list[i])  #convert the values to float
    p = calculate_p(px, py, pz)  #calculate the momentum
    pt = calculate_pT(px, py)  #calculate the transverse momentum   
    ps = calculate_pseudorapidity(p, pz)  #calculate the pseudorapidity
    phi = calculate_azimuthal_angle(px, py)  #calculate the azimuthal angle 
    particle_type = check_type(pdg_code)  #check the type of particle based on the pdg code

    if particle_type is None:
        print(f"Particle type:, {particle_type}, Momentum: {p:.10f}, Transverse Momentum: {pt:.10f}, Pseudorapidity: {ps:.10f}, Azimuthal Angle: {phi:.10f}")
