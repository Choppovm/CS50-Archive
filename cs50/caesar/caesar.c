#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>

bool only_digits(string text);
char rotate(char p, int k);
int main(int argc, string argv[])
{
    int k, len;
    string ptext;
    if (argc != 2 || !only_digits(argv[1])) {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    k = atoi(argv[1]);
    ptext = get_string("ptext: ");
    len = strlen(ptext);
    char ctext[len + 1];
    for (int i = 0; i< len; i++)
    {
        ctext[i] = rotate(ptext[i], k);
    }
    ctext[len] = '\0';
    printf("ciphertext: %s\n", ctext);
    return 0;
}
bool only_digits(string text)
{
    int len;
    len = strlen(text);
    for (int i = 0; i < len; i++){
        if (!isdigit(text[i])) {
            return false;
        }
    }
    return true;
}
char rotate(char p, int k)
{
    char pi, c, ci;
    if (isupper(p)) {
        pi = p - 65;
        ci = (pi + k)%26;
        c = ci + 65;
    }
    else if (islower(p)) {
        pi = p - 97;
        ci = (pi + k)%26;
        c = ci + 97;
    }
    else {
        return p;
    }
    return c;
}
