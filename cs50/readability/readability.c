#include <string.h>
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int sentencecount(string text);
int wordcount(string text);
int lettercount(string text);
int main(void)
{
    string text;
    int letters, words, sentences, index;
    double L, S;
    text = get_string("Text:");
    letters = lettercount(text);
    words = wordcount(text);
    sentences = sentencecount(text);
    L = letters/(float)words * 100;
    S = sentences/(float)words * 100;
    index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index > 16)
        printf("Grade 16+\n");
    else if (index < 1)
        printf("Before Grade 1\n");
    else
        printf("Grade %i\n", index);
}
int lettercount(string text)
{
    int len, count = 0;
    len = strlen(text);
    for (int i = 0; i< len; i++)
    {
        if (isalpha(text[i]) != 0)
            count ++;
    }
    return count;
}
int wordcount(string text)
{
    int len, count = 0;
    len = strlen(text);
    for (int i = 0; i< len; i++)
    {
        if (text[i] == ' ')
            count ++;
    }
    count ++;
    return count;
}
int sentencecount(string text)
{
    int len, count = 0;
    len = strlen(text);
    for (int i = 0; i< len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
            count ++;
    }
    return count;
}
