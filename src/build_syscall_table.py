#!/usr/bin/env python3

"""
This script looks through a user's unistd_64.h and maps system call numbers to
system call names. It prints an array of system call names where the indices of
the array correspond to the system call number. A user looking for the
appropriate header file should look for a unistd_{X}.h containing lines that
look as follows:
  #define __NR_read 0
  #define __NR_write 1
or more generally:
  #define __NR_{syscall_name} {syscall_num}
This is likely provided as part of your distribution's kernel headers package.
In Arch this is 'linux-headers' and is found here:
/usr/lib/modules/{kernel-version}-ARCH/build/arch/x86/include/generated/uapi/asm/
"""

#TODO: Needs to work with unistd_x32.h or whatever it's called

import sys
import re

def get_syscalls(unistd_h):
    inc = re.compile('^#define\s*__NR_(\w+)\s*(\d+)')
    syscalls = {}
    for line in open(unistd_h):
        match = inc.match(line)
        if match:
            (name, number) = match.groups()
            syscalls[int(number)] = name
    return syscalls

def print_syscalls(syscalls):
    max_syscall_name_len = max([len(name) for (num, name) in syscalls.items()])
    syscall_arr_size = len(syscalls)
    print('\n#define SYSCALLS_ARR_SIZE {}\n'.format(syscall_arr_size))
    print('const char syscalls[{}][{}] = {{'
            .format(syscall_arr_size, max_syscall_name_len))
    for ix in range(0, len(syscalls)):
        comma = ',' if ix != syscall_arr_size - 1 else ''
        content = '    "{}"'.format(syscalls[ix]) if syscalls[ix] else '    ""'
        print('{}{}'.format(content, comma))
    print('};\n')

def main(unistd_h):
    syscalls = get_syscalls(unistd_h)
    print_syscalls(syscalls)

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print('Usage: {} /path/to/unistd_64.h'.format(sys.argv[0]))
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
