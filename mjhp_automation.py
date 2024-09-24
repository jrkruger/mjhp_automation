#!/usr/bin/python3
#mjhp_automation.py
#In order to use, call: mjhp_auto.py  <Compound> , <Valence Electron Count> , <Pearson Symbol> ,  <Number of Data Sets> , <HKL Grid> , <HKL grid> ...
import os
import sys 
import time
import glob
import subprocess
import re


location = "./"


def modifile(filename, action, lines=None):
     # Reads, writes, or appends a file
     if action == "r":
         with open(filename, "r") as file:
             lines = file.readlines()
         return lines
     else:
         if lines is not None:
             with open(filename, action) as file:
                 file.writelines(lines)
             return 1
         else:
             return 0
def log(lines):
     global location
     # Creates or appends the log file
     if os.path.isfile(location + "automjhp.log") == False:
         modifile(location + "automjhp.log", "w", lines)
     else:
         modifile(location + "automjhp.log", "a", lines)


lines = ["This is a Test\n"]
lines.append("This is a Second Test\n")

#ADD FILES#
os.system("cp CPPrep_Equil/*in .")
os.system("cp CPPrep_Equil/*out .")
lines.append("files are now in the compound directory, allowing the script to proceed")

#System Arguments
compound = sys.argv[1]
memory = sys.argv[2]

# Valence electron counts for the first 82 elements
valence_electrons = {
    1: 1,   2: 2,   3: 1,   4: 2,   5: 3,   6: 4,   7: 5,   8: 6,   9: 7,   10: 8,
    11: 1,  12: 2,  13: 3,  14: 4,  15: 5,  16: 6,  17: 7,  18: 8,  19: 1,  20: 2,
    21: 3,  22: 4,  23: 5,  24: 6,  25: 7,  26: 8,  27: 9,  28: 10, 29: 1,  30: 2,
    31: 3,  32: 4,  33: 5,  34: 6,  35: 7,  36: 8,  37: 1,  38: 2,  39: 3,  40: 4,
    41: 5,  42: 6,  43: 7,  44: 8,  45: 9,  46: 10, 47: 1,  48: 2,  49: 3,  50: 4,
    51: 5,  52: 6,  53: 7,  54: 8,  55: 1,  56: 2,  57: 3,  58: 4,  59: 5,  60: 6,
    61: 7,  62: 8,  63: 9,  64: 10, 65: 11, 66: 12, 67: 13, 68: 14, 69: 15, 70: 16,
    71: 3,  72: 4,  73: 5,  74: 6,  75: 7,  76: 8,  77: 9,  78: 10, 79: 1,  80: 2,
    81: 3,  82: 4
}

spgroups = {
    1: "aP", 2: "aP", 3: "mP", 4: "mP", 5: "mC", 6: "mP", 7: "mP", 8: "mC", 9: "mC", 10: "mP", 11: "mP", 12: "mC",
    13:"mP", 14: "mP", 15: "mC", 16: "oP", 17: "oP", 18: "oP", 19: "oP", 20: "oC", 21: "oC", 22: "oF",
    23: "oI", 24: "oI", 25: "oP", 26: "oP", 27: "oP", 28: "oP",29: "oP", 30: "oP", 31: "oP", 32: "oP",
    33: "oP", 34: "oP", 35: "oC", 36: "oC", 37: "oC", 38: "oA", 39: "oA", 40: "oA", 41: "oA", 42: "oF",
    43: "oF", 44: "oI", 45: "oI", 46: "oI", 47: "oP", 48: "oP", 49: "oP", 50: "oP", 51: "oP", 52: "oP",
    53: "oP", 54: "oP", 55: "oP", 56: "oP", 57: "oP", 58: "oP", 59: "oP", 60: "oP", 61: "oP", 62: "oP",
    63: "oC", 64: "oC", 65: "oC", 66: "oC", 67: "oC", 68: "oC", 69: "oF", 70: "oF", 71: "oI", 72: "oI",
    73: "oI", 74: "oI", 75: "tP", 76: "tP", 77: "tP", 78: "tP", 79: "tI", 80: "tI", 81: "tP", 82: "tI",
    83: "tP", 84: "tP", 85: "tP", 86: "tP", 87: "tI", 88: "tI", 89: "tP", 90: "tP", 91: "tP", 92: "tP",
    93: "tP", 94: "tP", 95: "tP", 96: "tP", 97: "tI", 98: "tI", 99: "tP", 100: "tP", 101: "tP", 102: "tP",
    103: "tP", 104: "tP", 105: "tP", 106: "tP", 107: "tI", 108: "tI", 109: "tI", 110: "tI", 111: "tP", 112: "tP",
    113: "tP", 114: "tP", 115: "tP", 116: "tP", 117: "tP", 118: "tP", 119: "tI", 120: "tI", 121: "tI", 122: "tI",
    123: "tP", 124: "tP", 125: "tP", 126: "tP", 127: "tP", 128: "tP", 129: "tP", 130: "tP", 131: "tP", 132: "tP",
    133: "tP", 134: "tP", 135: "tP", 136: "tP", 137: "tP", 138: "tP", 139: "tI", 140: "tI", 141: "tI", 142: "tI",
    143: "hP", 144: "hP", 145: "hP", 146: "hP", 147: "hP", 148: "hP", 149: "hP", 150: "hP", 151: "hP", 152: "hP",
    153: "hP", 154: "hP", 155: "hP", 156: "hP", 157: "hP", 158: "hP", 159: "hP", 160: "hP", 161: "hP", 162: "hP",
    163: "hP", 164: "hP", 165: "hP", 166: "hP", 167: "hP", 168: "hP", 169: "hP", 170: "hP", 171: "hP", 172: "hP",
    173: "hP", 174: "hP", 175: "hP", 176: "hP", 177: "hP", 178: "hP", 179: "hP", 180: "hP", 181: "hP", 182: "hP",
    183: "hP", 184: "hP", 185: "hP", 186: "hP", 187: "hP", 188: "hP", 189: "hP", 190: "hP", 191: "hP", 192: "hP",
    193: "hP", 194: "hP", 195: "cP", 196: "cF", 197: "cI", 198: "cP", 199: "cI", 200: "cP", 201: "cP", 202: "cF",
    203: "cF", 204: "cI", 205: "cP", 206: "cI", 207: "cP", 208: "cP", 209: "cF", 210: "cF", 211: "cI", 212: "cp", 
    213: "cP", 214: "cI", 215: "cP", 216: "cF", 217: "cI", 218: "cP", 219: "cF", 220: "cI", 221: "cP", 222: "cP", 
    223: "cP", 224: "cP", 225: "cF", 226: "cF", 227: "cF", 228: "cF", 229: "cI", 230: "cI" 
}  


def extract_integers_from_line(line):
    parts = line.split()
    integers = [int(part) for part in parts if part.isdigit()]
    return integers

def process_in_file(filename):
    global total_valence_electrons
    try:
        lines.append("Processing file: {}\n".format(filename))
        valence_counts = []  # List to store valence electron counts from 'znucl' line
        
        with open(filename, 'r') as file:
            for line in file:
                if "znucl" in line:
                    lines.append("Found 'znucl' in line from '{}': {}\n".format(filename, line.strip()))
                    atomic_numbers = extract_integers_from_line(line)
                    if atomic_numbers:
                        valence_counts = [valence_electrons.get(num, 0) for num in atomic_numbers]
                        for i, valence in enumerate(valence_counts):
                            lines.append("Atomic number {}: Valence electrons = {}\n".format(atomic_numbers[i], valence))

                if "typat" in line:
                    lines.append("Found 'typat' in line from '{}': {}\n".format(filename, line.strip()))
                    typat_values = extract_integers_from_line(line)
                    if typat_values:
                        typat_count = {typat: typat_values.count(typat) for typat in set(typat_values)}
                        for typat, count in typat_count.items():
                            if typat <= len(valence_counts):
                                valence_count = valence_counts[typat - 1]
                                
                                # Calculate vec and add it to total_valence_electrons
                                vec = valence_count * count
                                total_valence_electrons += vec
                                
                                lines.append("Typat value {} (Valence electrons {}): vec = {}\n".format(typat, valence_count, vec))
        
        # Print the total_valence_electrons outside the loop
        lines.append("Total valence electrons in the unit cell: {}\n".format(total_valence_electrons))
        #log(lines)
    except FileNotFoundError:
        lines.append("Error: The file '{}' was not found.\n".format(filename))
    except Exception as e:
        lines.append("An error occurred: {}\n".format(e))

#log(lines)

def process_out_file(filename):
    global spgroup
    try:
        lines.append("Processing file: {}\n".format(filename))
        with open(filename, 'r') as file:
            for line in file:
                if "spgroup" in line:
                    lines.append("Found 'spgroup' file\n")

                    spgroup_numbers = extract_integers_from_line(line)
                    if spgroup_numbers:
                        spgroup = spgroups.get(spgroup_numbers[0], "UNKOWN")
                        if spgroup_numbers[0] in [146, 148, 155, 160, 161, 166, 167]:
                           lines.append("Should be Rhombohedral\n")
                        lines.append("Space group found: {}\n".format(spgroup))
                    else:
                        return None
                    break
        if sgroup is None:
             lines.append(f"No 'spgroup' found in '{filename}'.\n")
    
    except FileNotFoundError:
        lines.append(f"Error: The file '{filename}' was not found.\n")
    except Exception as e:
        None
        #log(lines)

def main():
    global total_valence_electrons
    global spgroup
    total_valence_electrons = 0
    spgroup = 0

    in_files = glob.glob('*.in')
    if not in_files:
        lines.append("No *.in files found in the current directory.\n")
        return

    for filename in in_files:
        total_valence = process_in_file(filename)

    out_files = glob.glob('*.out')  
    if not in_files:
        lines.append("No *.out files found in the current directory.\n")
        return

    for filename in out_files:
        process_out_file(filename)

if __name__ == "__main__":
    main()

lines.append("{}\n".format(total_valence_electrons))
lines.append("{}\n".format(spgroup))
log(lines)
filename = "{}.mjin".format(compound)
with open(filename, "w") as f:
  lines = [
    "{}\n".format(compound),
    "{}\n".format(compound),
    "vec {}\n".format(total_valence_electrons),
    "{}\n".format(spgroup),
   ]
  f.writelines(lines)

#os.system("qsub -I -l mem=120gb -d.")
os.chdir("CPPrep_Equil")


def comment_out_lines(file_path, prefixes_to_comment):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            for prefix in prefixes_to_comment:
                if line.strip().startswith(prefix):
                    line = '! ' + line
                    break
            file.write(line)

# Specify the prefixes of lines you want to comment out
prefixes_to_comment = [
    "scalecart1",
    "scalecart2",
    "scalecart3",
    "prtvol",
    "ndtset",
    "ngfft"
]

# Use glob to find all files that match the pattern
file_paths = glob.glob('*.in')

# Apply the commenting function to each file
for file_path in file_paths:
    comment_out_lines(file_path, prefixes_to_comment)

location = "../"

os.chdir("..")
os.system("mkdir " + "spt")
os.chdir("spt")
os.system("cp  ../CPPrep_Equil/{}.in .".format(compound))
os.system("cp  ../CPPrep_Equil/{}.files .".format(compound))

os.system("ssh kestrel 'cd cp_data/{}/spt; qabinit7 -np 12 -f *files' 2> /dev/null >> spt_calc.log".format(compound))

# Extract the job_id from the log file
job_id = None

# Open the log file
with open('spt_calc.log', 'r') as file:
    for line in file:
        # Use re.search to fin
# the line that contains '.kestrel.chem.wisc.edu'
        job = re.search(r'(\d+)\.kestrel\.chem\.wisc\.edu', line)
        if job:
            # Extract the number and set it as job_id
            job_id = job.group(1)
            break

# Print the job_id or perform further actions with it
if job_id:
    lines.append(f"job_id: {job_id}\n")
else:
    lines.append("job_id not found\n")
#log(lines)

# Function to check job status and update the text file
def check_job_status(job_id):
    os.system(f"ssh kestrel 'qstat {job_id}' 1> job_stat.txt 2> /dev/null")

# Loop to update the text file every 5 seconds until the job status is 'C'
job_finished = False
while not job_finished:
    check_job_status(job_id)
    lines.append("Running spt calculation, Please Wait\n")
    with open('job_stat.txt', 'r') as file:
        for line in file:
            if job_id in line:
                # Extract the status column
                status = line.split()[4]
                if status == 'C':
                    job_finished = True
                    break
    # Wait for 5 seconds before checking again
    if not job_finished:
        time.sleep(60)

os.system("rm job_stat.txt")
os.system("rm spt_calc.log")
time.sleep(5)
lines.append("Temporary Files Deleted\n")
os.chdir("..")
log(lines)

#more robust through command-line operations
if len(sys.argv) < 2:
    print("Usage: mjhp_automation.py <Compound> <Memory allocation (with unit)>")
    sys.exit(1)

#making new directories in the Terminal Window
os.system("mkdir " + "mjhp")
os.chdir("mjhp")
os.system("mkdir " + "HKL")
os.system("mkdir " + "2theta")
#os.chdir("HKL")

#2theta
os.chdir("2theta")
os.system("cp ../../spt/*_DEN ./{}_i_DEN".format(compound))
os.system("cp ../../spt/*in .")
os.system("cp ../../spt/*files .")
os.system("cp ../../*mjin .")


#filestructure2
#filename = "{}.mjin".format(compound)
#with open(filename, "w") as f:
 # lines = [
 #   "{}\n".format(compound),
 #   "{}\n".format(compound),
 #   "vec {}\n".format(total_valence_electrons),
 #   "{}\n".format(Pearson),
 #  ]
 # f.writelines(lines)
#print("Data has been written to", filename)

location = "../../"

os.system("prepare_mjhp2theta *mjin > /dev/null >> ../../automjhp.log")
lines.append("PReparing mjhp2theta *in file\n")
#log(lines)
time.sleep(10)

os.system("ssh kestrel 'cd cp_data/{}/mjhp/2theta; qabinit7 -np 12 -f *files' 2> /dev/null >> 2theta_calc.log".format(compound))

# Extract the job_id from the log file
job_id = None

# Open the log file
with open('2theta_calc.log', 'r') as file:
    for line in file:
        # Use re.search to find the line that contains '.kestrel.chem.wisc.edu'
        job = re.search(r'(\d+)\.kestrel\.chem\.wisc\.edu', line)
        if job:
            # Extract the number and set it as job_id
            job_id = job.group(1)
            break

# Print the job_id or perform further actions with it
if job_id:
    lines.append(f"job_id: {job_id}\n")
else:
    lines.append("job_id not found\n")
#log(lines)
# Function to check job status and update the text file
def check_job_status(job_id):
    os.system(f"ssh kestrel 'qstat {job_id}' 1> job_stat.txt 2> /dev/null")

# Loop to update the text file every 5 seconds until the job status is 'C'
job_finished = False
while not job_finished:
    check_job_status(job_id)
    lines.append("Preparing 2theta calculation, Please Wait\n")
    # Check if the job status is 'C' (Completed) by reading the contents of job_stat.txt
    with open('job_stat.txt', 'r') as file:
        for line in file:
            if job_id in line:
                # Extract the status column
                status = line.split()[4]
                if status == 'C':
                    job_finished = True
                    break

    # Wait for 5 seconds before checking again
    if not job_finished:
        time.sleep(30)

lines.append("2theta Prep Finished\n")
os.system("rm job_stat.txt")
os.system("rm 2theta_calc.log")
time.sleep(5)
lines.append("Temporary Files Deleted\n")
log(lines)

os.system("ssh kestrel 'cd cp_data/{}/mjhp/2theta; qmjhp2theta *mjin' > /dev/null >> ../../automjhp.log".format(compound))
lines.append("qmjhp2theta Running\n")
time.sleep(5)
os.system("find_reflections *mjin > /dev/null >> ../../automjhp.log")
lines.append("Reflections Appended to *mjin\n")
time.sleep(2)




#HKL
os.chdir("..")
os.chdir("HKL")
os.system("cp -l ../../spt/*WFK .")
os.system("cp ../../spt/*POT .")
os.system("cp ../../spt/*out .")
os.system("cp ../2theta/*mjin .")


#perform qmjhpHKL
os.system("ssh kestrel 'cd cp_data/{}/mjhp/HKL; qmjhpHKL *mjin -mem {}' > /dev/null >> ../../automjhp.log".format(compound, memory))


os.chdir("..")
os.chdir("..")
os.system("rm {}.in".format(compound))
os.system("rm {}.out".format(compound))
