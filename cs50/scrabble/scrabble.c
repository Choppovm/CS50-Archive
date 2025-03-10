#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int scorecalc(string word);
int main(void)
{
    string player1word = get_string("Player 1: ");
    string player2word = get_string("Player 2: ");
    int player1score = scorecalc(player1word);
    int player2score = scorecalc(player2word);

    if (player1score > player2score)
    {
        printf("Player 1 wins!\n");
    }
    else if (player2score > player1score)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie.\n");
    }
}
int scorecalc(string word)
{
    int len, pointsTotal = 0;
    len = strlen(word);
    for (int i = 0; i< len; i++)
    {
        if (isupper(word[i]))
        {
            pointsTotal += POINTS[word[i]- 65];
        }
        else if (islower(word[i]))
        {
            pointsTotal += POINTS[word[i]- 97];
        }
    }
    return pointsTotal;
}
