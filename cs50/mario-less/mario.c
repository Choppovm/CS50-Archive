#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int size, row, col, whitespace;
    do
    {
        size = get_int("Enter size here: ");
    }
    while (size < 1 || size > 8);

    for (row = 0; row < size; row++)
    {
        for (whitespace = 0; whitespace < size - row - 1; whitespace++)
        {
            printf(" ");
        }
        for (col = 0; col <= row; col++)
        {
            printf("#");
        }
        printf("\n");
    }
}
