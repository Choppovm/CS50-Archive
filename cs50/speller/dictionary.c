#include <stdbool.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include "dictionary.h"
#include <string.h>
#include <strings.h>

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
const unsigned int TABSIZE = 50000;
node *tab[TABSIZE];
bool check(const char *word)
{
    int ind = hash(word);
    node *cr = tab[ind];
    for (node *temp = cr; temp != NULL; temp = temp->next)
    {
      if (strcasecmp(temp->word,word) == 0)
        {
            return true;
        }
    }
    return false;
}
unsigned int hash(const char *word)
{
    unsigned int hvalue = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hvalue += tolower(word[i]);
        hvalue = (hvalue * tolower(word[i])) % TABSIZE;
    }
    return hvalue;
}
int counter = 0;
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "There has been an error");
        return false;
    }
    char wordlist[LENGTH + 1];
    while (fscanf(file, "%s", wordlist) != EOF)
    {
        counter++;
        node *nN = malloc(sizeof(node));
        if (nN == NULL)
        {
            return 1;
        }
        strcpy(nN->word, wordlist);
        nN->next = NULL;
        int ind = hash(wordlist);
        if (tab[ind] == NULL)
        {
            tab[ind] = nN;
        }
        else
        {
            nN->next = tab[ind];
            tab[ind] = nN;
        }
    }
    fclose(file);
    return true;
}
unsigned int size(void)
{
    return counter;
}
bool unload(void)
{
    node *tmp = NULL;
    node *cr = NULL;
    for (int i = 0; i < TABSIZE; i++)
    {
        cr = tab[i];
        while (cr != NULL)
        {
           tmp = cr;
            cr = cr->next;
           free(tmp);
        }
    }
    return true;
}
