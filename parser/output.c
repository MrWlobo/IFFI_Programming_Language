#include<stdio.h>
#include<math.h>
#include<stdbool.h>
int main() {
int myFunc(int a, int b, int c) {
c = (a + b);
return c;
}
int fa = 7;
while (true) {
fa = (fa + 8);
if ((fa > 100)) {
break;
}
printf("%d\n", (2 + 1));
}
if ((fa < 200)) {
myFunc(fa, fa, fa);
}
return 0;
}