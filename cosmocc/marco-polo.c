#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc > 1 && strcmp(argv[1], "Marco") == 0) {
        printf("Polo\n");
    } else {
        printf("Usage correct way: marco-polo Marco\n");
    }
    return 0;
}