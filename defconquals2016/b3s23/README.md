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

### Headers

```bash
$ docker run -i legitbs/b3s23
Welcome to b3s23.  Enter x,y coordinates.  Enter any other character to run.
```

