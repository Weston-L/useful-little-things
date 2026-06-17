################   SPLIT BIG FILES INTO SMALLER CHUNKS IN NOTEPAD++ WITH THIS PYTHON SCRIPT  ####################

"""
Step 1: Install the Python Script Plugin: Open Notepad++. Go to the top menu and select Plugins > Plugins Admin... In the search bar, type Python Script. Check the box next to Python Script and click Install in the top right.Notepad++ will prompt you to restart. Click Yes.

Step 2: Create the Script: Open the large text file you want to split in Notepad++.Go to Plugins > Python Script > New Script. Name your script (for example: split_file.py) and click Save. Copy and paste the code into the empty script file that opens.  Save the script.

Step 3: Run the Script: Click back onto the tab containing your large text file. Go to Plugins > Python Script > Scripts. Click on split_file (or whatever you named it). The script will instantly run in the background.  A success message will pop up when it finishes.

"""

import os

# Define how many lines you want per file
LINES_PER_FILE = 1000

# Get the folder and filename of the currently open big file
current_file = notepad.getCurrentFilename()
file_dir, file_name = os.path.split(current_file)
name_part, ext_part = os.path.splitext(file_name)

# Ensure the file is saved and we have a valid path
if os.path.exists(current_file):
    # Define a clean sub-folder path
    output_folder = os.path.join(file_dir, "{}_split_chunks".format(name_part))
    
    # Create the folder if it doesn't already exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    part_num = 1
    line_count = 0
    out_file = None
    
    try:
        # Open the 1.6GB file line by line (memory efficient)
        with open(current_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                # If we've hit 1000 lines or it's the first file, open a new chunk file
                if line_count % LINES_PER_FILE == 0:
                    if out_file:
                        out_file.close()
                    
                    # Target the new sub-folder for the output chunks
                    new_filename = os.path.join(output_folder, "{}_part{}{}".format(name_part, part_num, ext_part))
                    out_file = open(new_filename, 'w', encoding='utf-8')
                    part_num += 1
                
                # Write the single line to the current chunk
                out_file.write(line)
                line_count += 1
                
        # Close the final file chunk when done
        if out_file:
            out_file.close()
            
        notepad.messageBox("Done! Created folder:\n{}\n\nSplit into {} files.".format(output_folder, part_num - 1), "Success")
        
    except Exception as e:
        if out_file:
            out_file.close()
        notepad.messageBox("Error: " + str(e), "Script Failed")
else:
    notepad.messageBox("Please save your big file to your computer first.", "Error")
