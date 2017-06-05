This is a solution for the Dorabot Programming Task, done by Vardi Adi.

The two scripts, stringGenerator.py and stringProcessor.py solve the two parts of the task. They should be executable using basic python tools. The scripts were written using python 2.7.

--------------------------------------------
stringGenerator.py:
Generates random strings with random length (between minL and maxL) and writes them into the output file ./data.txt. The strings are delimited by \n (new line) and are composed from A-Z and a-z (extendable easily in the code).
The strings are generated using multiprocessing. Multiple jobs are created, each in charge a fixed number of strings, for a total of at least 4MB of strings (in the extreme case where all generated strings have the shortest allowed length). As all the strings are concatenated, the 37 Bytes overhead per string only exists once per 4MB, and thus is neglected.
The generation of the data is the most resource intensive, as the strings must be generated using random algorithms and kept in the RAM. This is another advantage of dividing the strings into 4MB packets, as the memory can be liberated and the jobs can be spread over all available cores and optimized using the CPU task manager. 
A single job is in charge of writing the strings into a file, so no collisions between different threads can occur. As the writing demands less resources than the generation, it can keep up with the queue. Once data was generated in the amount specified when starting the script, the writer stops.
The completion time is also calculated, as well as a progress bar, which updates every time the writer thread finished writing a package.

Documentation:
String Generator
positional arguments:
  minL        Minimum string length
  maxL        Maximum string length
  memory      Amount of strings to generate in GBs

example: python stringGenerator.py 4 8 3

--------------------------------------------
stringProcessor.py
Processes a file full of strings: Each line in the input file is processed by calling the expensiveFunc(line) function. For this implementation the expensiveFunc() is just a time delay, whose length is defined in the command line arguments. The strings are then sorted alphabetically, and written into the output file ./processOutput.txt.
In order to keep the sorting algorithm simple, python sorted() algorithm is used. This algorithm while efficient and fast, loads th file into the RAM, so cannot be used flawlessly for very big databases.
Multiprocessing is again used, similarly for the previous program - each expensiveFunc() is a separate job with an additional job for writing. This enables parallel processing of the strings, which will be very advantageous if expensiveFunc() was a heavy function.
The completion time is also calculated, as well as a progress bar, which updates every time the a processing function is done.

Documentation:
String Generator
positional arguments:
  timeDelay   time delay for each string (in seconds)
  inputFile   Input file

example: python stringProcessor.py 1 /home/adi/Desktop/Dorabot/processInput.txt

--------------------------------------------
Example input and output files are given in the repository.
