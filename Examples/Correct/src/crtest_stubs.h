#ifndef CRTEST_STUBS_H
#define CRTEST_STUBS_H
/***********************************************************************
    MODULE HISTORY

FILE NAME:  crtest_stubs.h
Project: CR Test (UNIT TESTER)
Project No.:

Date:       Name:                 Change:
11/09/2018  Chris Roberts         Created original Module

******************************************************************************************/
/**
\function
 
\brief      This header file contains all the function prototypes for all CR Test internal
            functions. The ones with "UserStubs" in the function name are located in the 
            crtest_stubs.c file and contents is user defined. All other functions are auto
            generated using the templates defined in the testcase_tp.c. These functions are 
            called by main.c and are NOT required by the user.

\description


******************************************************************************************/
#include <stdint.h>

//*************** INTERNAL FUNCTION DO NOT TOUCH *****************************************
void TestCase_Stimulate( const uint32_t testClock );

void TestCase_InitUserStubs( void );

void TestCase_PostStimulusUserStubs( const uint32_t testClock );

void TestCase_CyclicUserStubs( const uint32_t testClock );

void TestCase_PreExpectedUserStubs( const uint32_t testClock );

uint8_t TestCase_Expected( const uint32_t testClock, uint32_t * const NumberPassed, uint32_t * const NumberFailed  );

char * TestCase_GetNamePointer( void );

char TestCase_GetNameLength( void );
//*************** INTERNAL FUNCTION DO NOT TOUCH *****************************************


#endif