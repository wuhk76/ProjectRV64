# ProjectRV64
Experimental RISC-V RV64IM emulator written in Python.

## Usage
This is  a module that emulates a basic RISC-V 64 bit CPU, plus the M extension for integer multiplication and division. The code is able to execute RISC-V ASM from a file or list, and store the results in the memory and registers. 
The emulator can only support true instructions, so it cannot execute pseudo-ops such as li, mv, etc. However, the ebreak command can make it exit. Using a mid-tier Intel Core I3 with PyPy3, the program can run at 1 million instructions per second. The module can be imported with the line:
####
	from projectrv64 import rv64
in the Python script, as long as the module "projectrv64.py" is in the same directory. Using PyPy to execute the program could increase the speed about 2-  4x. It can be downloaded with this link:
####
	https://pypy.org/download.html
### Variables
#### Registers
Registers in the form of a dictionary, and the keys are under the alias names such as a0. To make the register assign a value, this line can be added in the script:
####
	some_variable = rv64.registers['register_name']
where "register_name" is the alias name of a register. Although the registers are under alias names, a name such as x10 can also be use in the ASM. Registers are cleared by default every new execution.
#### Memory
The memory is stored as rv64.mem and is stored by a bytearray of 16MB. It is cleared by default every new execution.
### Functions
#### Execute
	rv64.execute(asm, pc = 0, mem = None, imax = 0, debug = False)
This function can execute an ASM, which could be a file path or a list of instructions. The pc option controls the program count, changing the instruction that executes. The mem option allows for loading of memory, and uses the default memory of 16 MB if none. 
The imax allows the number of max instructions to be executed, with 0 as no limit. If the debug option is set to True, the program would print the instructions as it executes.