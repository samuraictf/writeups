justintime was in the pwnable which means that there is a bug that will enable reading of a 'flag' file on the filesystem. Running the program gives a prompt 'Enter command:'. Trying 'help', '?', 'h' doesn't produce any results so reverse engineering was necessary.

The available commands (initialized in 0x08058740) are:

* quit or q
* process or p
* sleep or s
* wake or w
* log or l

Looking at the various command details and arguments the full possibilities are:

* process <worker> <task> <paramaters>  (0x08058493)
* log <on|off> (0x08058384)
* the other commands do not take paramaters

The tasks possible are
* gcd - computes the greatest common divisor
* lcd - least common denominator (also known as LCM)
* prime - Checks if the number(s) are prime

Running various commands/reversing reveals that the program is multithreaded and has 4 workers. The main UI thread communicates with the workers through a structure and a global state variable. The structure (0x0812b580) has the following layout:
```c
struct thread_cmd {
	uint8_t task; //identified gcd, prime, or lcd
	uint8_t num_arguments;
	uint8_t pad[2];
	uint32_t arguments[4];
} commands[5];
```
while there are structures for 5 workers, only indexes 1 through 4 are used.


Inspecting how arguments are put into the structure shows something interesting:
```c
    eax = sub_8056cac(arg_offset_x4);
    if (LOBYTE(eax > 0x8 ? 0xff : 0x0) != 0x0) {
            sub_8081270("Too many arguments!");
            eax = 0x0;
    }
    else {
            var_16 = sub_8056cac(arg_offset_x4) - 0x3; //Number of actual arguments
            *(int8_t *)(((var_20 << 0x2) + var_20 << 0x2) + 0x812b580) = LOBYTE(var_31 & 0xff); // Set the task
            *(int8_t *)(0x1 + ((var_20 << 0x2) + var_20 << 0x2) + 0x812b580) = LOBYTE(var_16); //Set the number of arguments... 
            var_24 = 0x0;
            do {
                    if (var_24 >= var_16) { 
                        break;
                    }
                    *((var_24 + (var_20 << 0x2) + var_20) * 0x4 + 0x812b584) = sub_8076280(sub_805ca90(sub_8058e1c(arg_offset_x4, var_24 + 0x3)), 0x0, 0xa); //store the argument
                    var_24 = var_24 + 0x1;
            } while (true);
            eax = sub_807ff30("Task %s sent to worker %d\n", sub_805ca90(sub_8058e1c(arg_offset_x4, 0x2)), var_20);
    }
    goto loc_80586af;
```
This is dissassembly from Hopper, but what is happening is that it's checking the number of command line 'word', and if it's greater than 8 then it errors. But if you recall, the process command takes the worker number, the task and then arguments. So including the command process, it should only have 7 arguments if all 4 members of the struct are used - e.g. 'process 3 gcd 5 20 990 197348145'. So this could be a buffer overflow. And looking at the loop reveals that yes, there is a buffer overflow when processing the arguments. But if we think about it, the commands structure is an array so overflow would just overflow into the next workers' task number.... except for worker 4. 

Inspecting what is after the structure reveals the global state variable. The global state variable (0x0812b5e4) is used to indicate if the workers should process commands (=0), sleep (=1), or exit (=2). Looking at the worker thread's main function (0x08057f68) shows that the variable is checked to be 0, 1 or 2. It is then used as index into a function pointer table (0x81284c0) for the worker to do what is necessary.

It's too bad the value is checked... but wait.. this is a multithreaded program! If we could get a thread to check the variable, then another thread set it to something that isn't 0,1,2; we could potentially control a function pointer! And we can make it even more likely by turning logging on which logs to disk and may cause more task switches.

Since we have complete control of the index used in the function table, we can set it to a number which will then point to memory under our control - the arguments list for a worker is the perfect spot as we can put any 32 bit value in there and they are not changed until we send another command. Determining what to set the address there is the next step. Looking at the arguments passed via the function pointer call reveals that the first function argument is a pointer to the task arguments.. so we also get control of 32 bytes of data passed by pointer to a function.. why that's perfect for using system.

Finding system is easy by finding cross references to the string '/bin/sh'.


So the final exploit should:

* Turn logging on
* Set a worker's arguments to the address of system
* Set another worker's arguments with 32 bytes of command for system
* Overflow worker 4's arguments with the (offset state_table - &&system)/4



