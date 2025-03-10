#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int HEADSIZE = 44;

int main(int arr1, char *arr2[])
{
    if (arr1 != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }
    FILE *it = fopen(arr2[1], "r");
    if (it == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    FILE *ot = fopen(arr2[2], "w");
    if (ot == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    float fa = atof(arr2[3]);
    uint8_t header[HEADSIZE];
    fread(&header, sizeof(header), 1, it);
    fwrite(&header, sizeof(header), 1, ot);
    int16_t bf;
    while (fread(&bf, sizeof(bf), 1, it))
    {
        bf *= fa;
        fwrite(&bf, sizeof(bf), 1, ot);
    }
    fclose(it);
    fclose(ot);
}
