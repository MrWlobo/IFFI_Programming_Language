#include<stdio.h>
#include<math.h>
#include<stdbool.h>
#include<stdlib.h>
//Int List
typedef struct intlist {
  int data;
  struct intlist* next;
} int_list_t;

void intAdd(int_list_t* list, int element) {
    int_list_t * current = list;
    while (current->next != NULL) {
        current = current->next;
    }
    current->data = element;
    current->next = (int_list_t*) malloc(sizeof(int_list_t));
    current->next->next = NULL;
}

int intLength(int_list_t* list) {
    int_list_t * current = list;
    int len = 0;
    while(current->next != NULL) {
        len++;
        current = current->next;
    }
    return len;
}

int intGet(int_list_t* list, int index) {
    int_list_t * current = list;
    int current_index = 0;
    while(current->next != NULL) {
        if(current_index == index) {
            break;
        }
        current_index++;
        current = current->next;
    }
    return current->data;
}
//Int List
typedef struct intlist {
  int data;
  struct intlist* next;
} int_list_t;

void intAdd(int_list_t* list, int element) {
    int_list_t * current = list;
    while (current->next != NULL) {
        current = current->next;
    }
    current->data = element;
    current->next = (int_list_t*) malloc(sizeof(int_list_t));
    current->next->next = NULL;
}

int intLength(int_list_t* list) {
    int_list_t * current = list;
    int len = 0;
    while(current->next != NULL) {
        len++;
        current = current->next;
    }
    return len;
}

int intGet(int_list_t* list, int index) {
    int_list_t * current = list;
    int current_index = 0;
    while(current->next != NULL) {
        if(current_index == index) {
            break;
        }
        current_index++;
        current = current->next;
    }
    return current->data;
}
int main() {
int myFunc(int a, int b, int c) {
c = a + b;
return c;
}
int fa = 7;

while (true) {
fa = fa + 8;
if ((fa > 100)) {
printf("%d\n", fa);
break;
}
}
int_list_t lista;lista.next = NULL;
intAdd(&lista, 1);
intAdd(&lista, 2);
intAdd(&lista, 3);
intAdd(&lista, 8);
intAdd(&lista, 99);
intAdd(&lista, 123);
intAdd(&lista, 90001);
int_list_t* current_lista = &lista;
int current_lista_data = current_lista->data;

int_list_t lista1;lista1.next = NULL;
intAdd(&lista1, 3);
intAdd(&lista1, 2);
intAdd(&lista1, 1);
int_list_t* current_lista1 = &lista1;
int current_lista1_data = current_lista1->data;

for (int i = 0; i < intLength(&lista); i++) {
current_lista_data = current_lista->data;

current_lista = current_lista->next;

for (int j = 0; j < intLength(&lista1); j++) {
current_lista1_data = current_lista1->data;

current_lista1 = current_lista1->next;

printf("%d\n", current_lista1_data+current_lista_data);
}
current_lista1 = &lista1;
current_lista1_data = current_lista1->data;
}
current_lista = &lista;
current_lista_data = current_lista->data;
return 0;
}