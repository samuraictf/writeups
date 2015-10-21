## risky, 300 point reversing challenge from hitcon quals 2015
#### by dropkick from team Samurai

`risky` turned out to be a [RISC-V](http://riscv.org/) binary (hitcon team is good at naming challenges).  Never having dealt with this architecture before, I burned a good bit of time attempting to get all the available [RISC-V toolchains](https://github.com/riscv) functional, which was unnecessary.  In the end we couldn't even get the `spike` simulator to work correctly; we resorted to pure static reversing.

#### Analysis 
We were able to use `riscv64-unknown-elf-objdump` from `riscv-tools` to at least get a disassembly.  Finding the call to `__libc_start_main` gets you the address of `main()`, which is at the top of the `.text` section.  `main()` is the only real function in the binary.  `main()` begins by prompting the user for input and ensuring the input takes the form `XXXX-XXXX-XXXX-XXXX-XXXX`.  Once that's complete, each of the five sequences of 4 chars each is loaded into a register and treated as a single 32-bit value.

#### Extracting constraints
A number of simple checks are done on the input values.  The full set of constraints can be viewed in solve.py.  Learning point: the `lui` instruction in RISC-V means load *upper* immediate, NOT load *unsigned* immediate.

### XOR'ing and flag generation
When the constraints are met, the program prints `Generating flag` and then goes though a loop that xors each of the five 32-bit inputs with values that are calculated and saved on the stack (again see the solve script).  The program then spits out the flag, which should be `hitcon{dYauhy0urak9nbavca1m}`
