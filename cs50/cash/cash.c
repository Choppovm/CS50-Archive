#include <cs50.h>
#include <stdio.h>

int calculatequarterval(int centsval);
int main(void)
{
    int centsval;
    do
    {
        centsval = get_int("Enter cash here: ");
    }
    while (centsval <= 0);
    int quarterval = calculatequarterval(centsval);
    printf("Quarters %i\n", quarterval);
}
int calculatequarterval(int centsval)
{
    int quarterval = 0;
    while (centsval != 0)
    {
        while (centsval >= 25)
        {
            quarterval++;
            centsval = centsval - 25;
        }
        while (centsval >= 10 && centsval < 25)
        {
            quarterval++;
            centsval = centsval - 10;
        }
        while (centsval >= 5 && centsval < 10)
        {
            quarterval++;
            centsval = centsval - 5;
        }
        while (centsval >= 1 && centsval < 5)
        {
            quarterval++;
            centsval = centsval - 1;
        }
    }
    return quarterval;
}
