#!/usr/bin/env python3

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
    print('const char syscalls[{}][{}] = {{'
            .format(len(syscalls), max_syscall_name_len))
    for ix in range(0, len(syscalls)):
        comma = ',' if ix != len(syscalls) - 1 else ''
        content = '    "{}"'.format(syscalls[ix]) if syscalls[ix] else '    ""'
        print('{}{}'.format(content, comma))
    print('};')

def main(unistd_h):
    syscalls = get_syscalls(unistd_h)
    print_syscalls(syscalls)

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        #TODO: Probably ought to indicate to the user where this might be, and
        # what they might expect to see. For arch, install linux-headers
        # package and look in:
        # /usr/lib/modules/{kernel-version}-ARCH/build/arch/x86/include/generated/uapi/asm/
        print('Usage: {} /path/to/unistd_64.h'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
