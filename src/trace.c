
#define _XOPEN_SOURCE 700

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

#include <string.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <unistd.h>

void die(char* message){
    printf("Error. Message: '%s'\n", message);
    exit(-1);
}

/* argc   - the same argc passed to the program
 * offset - the index into argv of the file name to execute
 * argv   - the same argv passed to the program. It is expected that all
 *          contents after argv[offset] are arguments to be provided to the
 *          child application
 */
void do_tracee(int argc, int offset, char** argv) {
    /* Build an array suitable to pass to execvp. See man execvp for details. */
    int args_length = (argc - offset + 1);
    char** copied_args = malloc(args_length * sizeof(char*));
    if (NULL == copied_args) {
        die("Couldn't allocate memory for tracee arguments.");
    }
    /* Copy the arguments we're interested in; null-terminate */
    memcpy(copied_args, argv + offset, (args_length - 1) * sizeof(char*));
    copied_args[args_length - 1] = (char*)NULL;
    if (ptrace(PTRACE_TRACEME, NULL, NULL, NULL) < 0) {
        die("Error calling ptrace in child.");
    }
    execvp(argv[offset], copied_args);
}

void do_trace(pid_t child_pid) {
    int child_status;
    struct user_regs_struct child_regs;

    wait(&child_status);

    while (1) {
        if (ptrace(PTRACE_SYSCALL, child_pid, NULL, NULL) < 0) {
            die("Error attempting to trace child");
        }

        if (WIFEXITED(child_status)) {
            printf("Child exited. Status: %d", child_status);
            break;
        }

        wait(&child_status);

        if (ptrace(PTRACE_GETREGS, child_pid, NULL, &child_regs) < 0) {
            die("Error attempting to read child registers");
        }

    }
}

int main(int argc, char* argv[])
{
    /* Print invocation */
    printf("Invocation:");
    for (int i=0; i<argc; i++)
    {
        printf(" %s", argv[i]);
    }
    printf("\n");

    /* Begin tracing */
    pid_t pid = fork();
    switch (pid) {
        case -1:
            die("Fork error");
            break;
        case 0:
            do_tracee(argc, 1, argv);
            break;
        default:
            do_trace(pid);
            break;
    }
    return 0;
}

