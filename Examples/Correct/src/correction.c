
#include <stdint.h>

#include "correction.h"


// Correction for x, y = x + (x/a)
uint16_t correction( const uint16_t x, const int8_t a)
{
    uint16_t result = 0;
    int16_t correction = 0;
    
    if( a != 0)
    {
        correction = x/a;
        if( x > correction )
        {
            result = (uint16_t)(x + correction);
        }
    }

    return(result);
}