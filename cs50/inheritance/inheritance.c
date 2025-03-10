#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct person
{
    struct person *parents[2];
    char alleles[2];
}
person;
const int GEN = 3;
const int INDENT_LENGTH = 4;
person *create_family(int generations);
void pfamily(person *p, int generation);
void free_family(person *p);
char rall();
int main(void)
{
    srand(time(0));
    person *p = create_family(GEN);
    pfamily(p, 0);
    free_family(p);
}
person *create_family(int generations)
{
    person *n = malloc(sizeof(person));
    if (n == NULL)
    {
        return NULL;
    }
    if (generations > 1)
    {
        n->parents[0] = create_family(generations - 1);
        n->parents[1] = create_family(generations - 1);
        n->alleles[0] = n->parents[0]->alleles[rand() % 2];
        n->alleles[1] = n->parents[1]->alleles[rand() % 2];
    }
    else
    {
        n->parents[0] = NULL;
        n->parents[1] = NULL;
        n->alleles[0] = rall();
        n->alleles[1] = rall();
    }
    return n;
}
void free_family(person *p)
{
    if (p == NULL){
        return;
    }
    free_family(p->parents[0]);
    free_family(p->parents[1]);
    free(p);
}
void pfamily(person *p, int generation)
{
    if (p == NULL)
    {
        return;
    }
    for (int i = 0; i < generation * INDENT_LENGTH; i++)
    {
        printf(" ");
    }
    printf("Generation %i, blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    pfamily(p->parents[0], generation + 1);
    pfamily(p->parents[1], generation + 1);
}
char rall()
{
    int r = rand() % 3;
    if (r == 0)
    {
        return 'A';
    }
    else if (r == 1)
    {
        return 'B';
    }
    else
    {
        return 'O';
    }
}
