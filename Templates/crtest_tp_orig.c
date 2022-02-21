/***********************************************************************
    MODULE HISTORY

FILE NAME:  crtest_tp.c
Project: CR Test (UNIT TESTER)
Version: 02.00

This is a template c file which contain pre determined structure types, 
arrays and function definitions ready to be populated by python. The 
structures, arrays and functions contains have key word which python 
replaces with the user types, variables and values. 

Date:       Name:                 Change:
11/09/2018  Chris Roberts         Created original Module
04/12/2018  Chris Roberts         Added evaluation Ranges (V02.00)

******************************************************************************************/
/**
\function
 
\brief      

\description


******************************************************************************************/
#include <stdint.h>
#include <stdio.h>

//Test stubs c file include to access the Module under test static variables / functions
#include "crtest_stubs.c"

#define NUMBER_OF_TEST_CASES    ##TestCase_NoTests##

#define NUMBER_OF_VARIABLES     ##TestCase_NoVariables##

#define NUMBER_OF_RANGE_ROWS    ##TestCase_NoRangeRows##

char testCaseName[] = "##TestCase_Name##";

char *testCaseString[NUMBER_OF_TEST_CASES] = ##TestCase_RawRowString##;

char testCaseReqString[] = "##TestCase_ReqString##";

typedef enum
{
    TC_STIMULUS = 0,   //Update variable from test case
    TC_EQUAL,          //Check variable is equal to test case
    TC_LESS,           //Check variable is less than test case
    TC_GREATER,        //Check variable is greater than test case
    TC_LESS_EQU,       //Check variable is less than or equal to test case
    TC_GREATER_EQU,    //Check variable is greater than or equal to test case
    TC_NOT_EQU,        //Check variable is Not equal to test case
    TC_RANGE_EQUAL,    //Check variable is equal to test case range
    TC_RANGE_NOT_EQU,  //Check variable is Not equal to test case range
    TC_NOTHING,
    TC_MAX
}TestCase_Control_en;

//This structure type contains the variable types from the users test case
typedef struct
{
##TestCase_ValueType##
}TestCase_ValueType;

//This structure type contains the control values (2 x time) and 
//enums one for each of the users variables from the test case
typedef struct
{
    uint32_t updateTime;
    uint32_t checkTime;
##TestCase_ControlType##
}TestCase_ControlType;

uint32_t TestNumber   = 0;

uint32_t RangeIndex  = 0;

// This array is auto-generated and contains the value from each user variable, from each row
// For range evaluations the value in this array are the minimum range
const TestCase_ValueType TestCase_Values[NUMBER_OF_TEST_CASES] =
{
##TestCase_Values##
};

// This array is auto-generated and contains the control (stimulus or evaluation) for value, from each row
const TestCase_ControlType TestCase_Control[NUMBER_OF_TEST_CASES] =
{
##TestCase_Control##
};

// This array is auto-generated and contains the maximum values from each user variable, from each row
// which require range evaluations. If a test case row don't contain a range evaluation then no row 
// is generated here. Also variables not requiring range evaluations will be set to 0.
#if (NUMBER_OF_RANGE_ROWS > 0)
const TestCase_ValueType TestCase_ValuesMax[NUMBER_OF_RANGE_ROWS] =
{
##TestCase_ValuesMax##
};
#endif

//Function prototypes
##TestCase_VarCheckFn1##static uint8_t TestCase_VarCheck_##VarName##( const TestCase_Control_en Value_Control, 
##TestCase_VarCheckFn1##                                              const ##VarType## TestCase_Value, 
##TestCase_VarCheckFn1###if (NUMBER_OF_RANGE_ROWS > 0)
##TestCase_VarCheckFn1##                                              const ##VarType## TestCase_ValueMax,
##TestCase_VarCheckFn1###endif
##TestCase_VarCheckFn1##                                              const ##VarType## Actual_Value);
##TestCase_VarCheckFn1##

void TestCase_Stimulate( const uint32_t testClock )
{
    if(TestCase_Control[TestNumber].updateTime == testClock) 
    {
##TestCase_StimulateFn##        if(TC_STIMULUS == TestCase_Control[TestNumber].##VarName##_Control)
##TestCase_StimulateFn##        {
##TestCase_StimulateFn##            ##VarName## = TestCase_Values[TestNumber].##VarName##;
##TestCase_StimulateFn##        }
    }
}

uint8_t TestCase_Expected( const uint32_t testClock, uint32_t * const NumberPassed_pt, uint32_t * const NumberFailed_pt )
{
    uint8_t allTestFinished = 0;
    uint32_t tempPassed = * NumberPassed_pt;
    uint32_t tempFailed = * NumberFailed_pt;
    
##TestCase_ExpectedV1##    uint8_t ##VarName##_check = 1;
    if(TestCase_Control[TestNumber].updateTime == testClock) 
    {
        //Check the variables which require checking
##TestCase_ExpectedFn##        ##VarName##_check = TestCase_VarCheck_##VarName##( TestCase_Control[TestNumber].##VarName##_Control,
##TestCase_ExpectedFn##                                                           TestCase_Values[TestNumber].##VarName##,
##TestCase_ExpectedFn###if (NUMBER_OF_RANGE_ROWS > 0)
##TestCase_ExpectedFn##                                                           TestCase_ValuesMax[RangeIndex].##VarName##,
##TestCase_ExpectedFn###endif
##TestCase_ExpectedFn##                                                           ##VarName##);
        
        //Check if a evaluation Range was used and if yes increament RangeIndex
        if( 
##TestCase_ExpectedV5##            (TestCase_Control[TestNumber].##VarName##_Control == TC_RANGE_EQUAL ) || (TestCase_Control[TestNumber].##VarName##_Control == TC_RANGE_NOT_EQU) ||
            0 )
        {
            RangeIndex++;
            if(RangeIndex > NUMBER_OF_RANGE_ROWS)
            {
                RangeIndex = NUMBER_OF_RANGE_ROWS;
            }
        }
        
        //Check that all required variables were as expected
        if( 
##TestCase_ExpectedV2##            ##VarName##_check &&
            1 )
        {
            //Passed Test Case output with just Actual
            printf("Raw Test Case: %s\n", testCaseString[TestNumber]);
            printf("Passes Actual: %d", TestCase_Control[TestNumber].updateTime);
##TestCase_ExpectedV3##            printf(", %d", TestCase_Values[TestNumber].##VarName##);
            printf("\n");
            
            tempPassed++;
            *NumberPassed_pt = tempPassed;
            
        }
        else
        {
            //Failed Test Case output with both expected and actual, 
            //add 3 to the TestNumber, 2 for the header rows in test case, + 1 as row start at 1 not 0
            printf("Test Case Row No: %d -> FAILED \n", TestNumber + 3);
            printf("Raw Test Case: %s\n", testCaseString[TestNumber]);
            printf("Failed Actual: %d", testClock);
##TestCase_ExpectedV4##            printf(", %d", ##VarName##);
            printf("\n");
            
            tempFailed++;
            *NumberFailed_pt = tempFailed;
        }

        
        //Update to the next test case 
        TestNumber++;
    }
    if(NUMBER_OF_TEST_CASES <= TestNumber)
    {
        allTestFinished = 1;
        printf("\nRequirements covered by this Test Case:\n%s\n", testCaseReqString);
    }
    return(allTestFinished);
}

##TestCase_VarCheckFn2##// Variable check function generated for ##VarName##
##TestCase_VarCheckFn2##static uint8_t TestCase_VarCheck_##VarName##( const TestCase_Control_en Value_Control, 
##TestCase_VarCheckFn2##                                              const ##VarType## TestCase_Value, 
##TestCase_VarCheckFn2###if (NUMBER_OF_RANGE_ROWS > 0)
##TestCase_VarCheckFn2##                                              const ##VarType## TestCase_ValueMax, 
##TestCase_VarCheckFn2###endif
##TestCase_VarCheckFn2##                                              const ##VarType## Actual_Value)
##TestCase_VarCheckFn2##{
##TestCase_VarCheckFn2##    uint8_t Value_Check = 1;
##TestCase_VarCheckFn2##    if(TC_EQUAL == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = (  TestCase_Value ==  Actual_Value );
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2##    else if(TC_LESS == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = (  TestCase_Value >  Actual_Value );
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2##    else if(TC_GREATER == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = (  TestCase_Value <  Actual_Value );
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2##    else if(TC_LESS_EQU == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = (  TestCase_Value >=  Actual_Value );
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2##    else if(TC_GREATER_EQU == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = (  TestCase_Value <=  Actual_Value );
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2##    else if(TC_NOT_EQU == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = (  TestCase_Value !=  Actual_Value );
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2###if (NUMBER_OF_RANGE_ROWS > 0)
##TestCase_VarCheckFn2##    else if(TC_RANGE_EQUAL == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = ((  TestCase_Value <=  Actual_Value ) && (  TestCase_ValueMax >=  Actual_Value ));
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2##    else if(TC_RANGE_NOT_EQU == Value_Control)
##TestCase_VarCheckFn2##    {
##TestCase_VarCheckFn2##        Value_Check = ((  TestCase_Value >  Actual_Value ) || (  TestCase_ValueMax <  Actual_Value ));
##TestCase_VarCheckFn2##    }
##TestCase_VarCheckFn2###endif
##TestCase_VarCheckFn2##    return(Value_Check);
##TestCase_VarCheckFn2##}
##TestCase_VarCheckFn2##

char * TestCase_GetNamePointer( void )
{
    return(testCaseName);
}

char TestCase_GetNameLength( void )
{
    return(sizeof(testCaseName));
}


