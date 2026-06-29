#include <stdio.h>
#include <math.h>
#include <time.h>

int random(int low, int high)
{
    double number = clock();
    double s = sqrt(high) * 32;
    for (int i; i < 60000; i++) {
        if (number < high) {
            number = number * number;
        }
        while (number > high) {
            number = number / s;
        }
    }
    if (number > high) {
        number = high;
    } else if (number < low) {
        number = low;
    }

    return number;
}
int main()
{
    int n = random(0, 1000000000);
    for (int i = 0; i < n; i++) {
        int t = random(0, 1000000);
        printf("Random number: %d\n",t);
        if (t < 10)
        {
            i = n;
        }
    }
    return 0;
}