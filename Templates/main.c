
#include <stdint.h>
#include <stdio.h>
#include "crtest_stubs.h"

char mainVersion[] = "01.00";

int main (void);

uint32_t testClock = 0;
uint32_t NumberPassed = 0;
uint32_t NumberFailed = 0;

int main (void)
{
    TestCase_InitUserStubs();
    
    //Cycle throught each test
    for(testClock = 0; (testClock < 0xFFFFFFFF); testClock++)
    {
        //Simulate the inputs
        TestCase_Stimulate( testClock );
        TestCase_PostStimulusUserStubs( testClock );
        
        //Call to function/s
        TestCase_CyclicUserStubs(testClock);
        
        //Check the output
        TestCase_PreExpectedUserStubs( testClock );
        if(1 == TestCase_Expected( testClock, &NumberPassed, &NumberFailed ))
        {
            break;
        }
    }

    if( 0 != NumberFailed )
    {
        printf("Test Complete: %d out of %d Tests Failed    ", NumberFailed, (NumberFailed+NumberPassed));
    }
    else
    {
        printf("\nTest Complete: %d out of %d Tests PASSED    ", (NumberFailed+NumberPassed),(NumberFailed+NumberPassed));
    }
    printf("Simulated test time: %dms \n\n", testClock);
    return(0);
}

