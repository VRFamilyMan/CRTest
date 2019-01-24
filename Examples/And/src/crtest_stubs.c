#include "crtest_stubs.h"
#include "common_crtest.h"

//Add User module under Test here. Include the c files if you wish to access static variables / functions 
#include "And.h"
#include "Or.h"

//User stubs as values only accessable via functions 
uint8_t aa,bb,cc,dd,ee;
uint8_t aa2,bb2,cc2,dd2,ee2;
uint8_t result;
uint8_t result2;

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

        result = And_5way(aa,bb,cc,dd,ee);

        result2 = Or_5way(aa2,bb2,cc2,dd2,ee2);

    }
}

//User populates if variable needs to be updated from the module via a functions or other type
void TestCase_PreExpectedUserStubs( const uint32_t testClock )
{

}


