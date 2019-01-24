#include "crtest_stubs.h"

//Add User module under Test here. Include the c files if you wish to access static variables / functions 


//User stubs as values only accessable via functions 
uint8_t TestValue,TestEvaluation;
uint16_t TestValue2,TestEvaluation2;
uint32_t TestValue3,TestEvaluation3;

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
    // Load Evaluation Value with the test Value so no external code required
    TestEvaluation  = TestValue;
    TestEvaluation2 = TestValue2;
    TestEvaluation3 = TestValue3;
}

//User populates if variable needs to be updated from the module via a functions or other type
void TestCase_PreExpectedUserStubs( const uint32_t testClock )
{

}


