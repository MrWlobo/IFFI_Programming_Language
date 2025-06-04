#include<stdio.h>
#include<math.h>
#include<stdbool.h>
#include<stdlib.h>
int main() {
int a = 10;

int b = 20;

int result = (a + b) * 2 - (b / a);

printf("%d\n", result);
bool condition = ((((a == 10) && (b != 15))) || !((a > b)));

printf("%d\n", condition);
int val = 5;

printf("%d\n", ++val);
printf("%d\n", val--);
printf("%d\n", val);
return 0;
}