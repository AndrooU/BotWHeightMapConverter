# BotWHeightMapConverter
Tool to easily obtain terrain height maps for use outside BotW.


Requirements:
- wszst     (https://szs.wiimm.de/wszst/)
- sarc      (https://pypi.org/project/sarc/)
- pillow    (https://pypi.org/project/Pillow/)
- kivy      (run "pip install kivy" and "python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew" in command prompt)
* wszst and sarc must be added to PATH for the included batch file to work



Setup Instructions:

Move the included batch file to your BotW Files in content/Terrain/A/MainField
and run it to decode and extract all .hght files. Move the generated 'terrain'
folder to the same directory as generate_map.py and gen_map_gui.py. (The batch
file will take several minutes to complete, and unpack about 1.1 GB worth of 
files)



Tool Usage:

Open a command prompt or powershell in the folder containing gen_map_gui.py and 
run "python gen_map_gui.py". Use the slider to select which level of detail you 
would like to use from zero as the entire map, and each LOD as 4^x map sections. 
Click and drag on the map to highlight the section would like to extract. You 
can change the LOD again or click generate to output a 16 bit depth grayscale 
PNG file of the chosen region



Other Information:
- Each map section is 256x256 pixels
- Generating the full LOD 8 map uses roughly 8 GB of RAM, so be careful with
larger LODs.



Credit:
- generate_map.py and Run This In Terrain A MainField.bat - Aaaboy97 2019
- gen_map_gui.py - toffeenose and Nomen Usoris 2019
