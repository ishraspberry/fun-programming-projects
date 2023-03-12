#include <stdlib.h> //standard stuff
#include <iostream> //
#include <pthread.h> //pthread_create(), pthread_join()
#include <cstring>
#include <vector>

using namespace std;
#define RNDARR 70000

int mysize;
int randArr[RNDARR];
int thrdC;//thread size
int sizeC;

pthread_mutex_t lox;

struct stuff{//stuff for the threading
    int start;
    int* arr;
};

void composite(int num){
    int count = 0;
    for(int m = 1; m <= num; m++){
        if(num%m == 0){
            count++;
        }
    }
    pthread_mutex_lock(&lox);
    if(count == 2){
        cout << num <<" is not composite\n";
    }
    else {
        cout << num << " is composite\n";
    }
    pthread_mutex_unlock(&lox);
}

void* confirm(void *s){
    struct stuff *mystuff;
    mystuff = (struct stuff*)s; 
    int start = mystuff->start;
    int* array = mystuff->arr;

    for(int x = start; x < sizeC; x += thrdC){
        composite(array[x]);
    }
    pthread_exit(0);
}


int main(int argc, char *argv[]){
    mysize = argc;//total number of arguments
    
    int sizing = mysize-2;//minus 2
    int checks = 1;//start from arg 1
    int count = 2;//count from here for argv
    
    char* arr = argv[checks]+1;
    thrdC = atoi(arr);
    int mydata[sizing];
    for(int x = count; x < mysize; x++){
        //cout << argv[x] <<endl;
        mydata[x-count] = atoi(argv[x]);
    }
    
    pthread_t threadID[thrdC];
    struct stuff td[thrdC];

    if(strcmp(argv[2],"pls") == 0){
        int myarray[RNDARR];
        for(int x = 0; x < RNDARR; x++){
            int rnd = rand()%40;
            myarray[x] = rnd;
        }
        sizeC = RNDARR;
        for(int x = 0; x < thrdC; x++){
            td[x].start = x;
            td[x].arr = myarray;
            pthread_create(&threadID[x], NULL, confirm, (void*)&td[x]);
        }
        for(int x = 0; x < thrdC; x++){
            pthread_join(threadID[x], NULL);
        }
        
    }

   else{
        sizeC = sizing;
        for(int x = 0; x < thrdC; x++){
            td[x].start = x;
            td[x].arr = mydata;
            pthread_create(&threadID[x], NULL, confirm, (void*)&td[x]);
        }
        for(int x = 0; x < thrdC; x++){
            pthread_join(threadID[x], NULL);
        }
   }
   return 0;
}