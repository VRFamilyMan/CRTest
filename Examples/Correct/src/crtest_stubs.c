#include "crtest_stubs.h"

//Add User module under Test here. Include the c files if you wish to access static variables / functions 
#include "correction.h"

//User stubs as values only accessable via functions 
int8_t a;
uint16_t x,result;
uint8_t dummy = 0;

//User populates if variable needs to be passed to the module via a function or other type
void TestCase_InitUserStubs( void )
{

}

//User populates if variable needs to be passed to the module via a function or other type
void TestCase_PostStimulusUserStubs( const uint32_t testClock )
{

}

//User populates if variable needs to be passed to the module via a function or other type
void TestCase_CyclicUserStubs( const uint32_t testClock )
{

    if(0 == (testClock%10))
    {
        result = correction(x,a);
    }
}

//User populates if variable needs to be updated from the module via a functions or other type
void TestCase_PreExpectedUserStubs( const uint32_t testClock )
{

}


