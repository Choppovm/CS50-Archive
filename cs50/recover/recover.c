#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if(argc!=2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    FILE*in=fopen(argv[1], "r");
    if(in==NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }
    FILE* out = NULL;
    BYTE buff[512];
    int jpeg=0;
    char fn[8]={0};
    while(fread(buff, sizeof(BYTE)*512, 1, in)==1)
    {
        if(buff[0]==0xFF&&buff[1]==0xD8&&buff[2]==0xFF&&(buff[3]&0xF0)==0xE0)
        {
            if(out != NULL)
            {
                fclose(out);
            }
                sprintf(fn, "%03d.jpg", jpeg++);
                out = fopen(fn, "w");
        }
       if(out != NULL)
       {
            fwrite(buff, sizeof(BYTE)*512, 1, out);
       }
    }
     if (out != NULL)
     {
      fclose(out);
     }
      fclose(in);
    return 0;
}
