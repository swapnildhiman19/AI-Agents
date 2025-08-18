#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Please pass some arguments when you run the program!\n");
        printf("Example: ./myprogram apple banana\n");
        return 1; 
    }
    
    printf("You provided %d argument(s):\n", argc - 1);
    for (int i = 1; i < argc; i++) {
        printf(" - Argument %d: %s\n", i, argv[i]);
    }
    
    return 0;
}
