
#include <stdint.h>

#include "Or.h"

uint8_t Or_5way( const uint8_t aa, const uint8_t bb, const uint8_t cc, const uint8_t dd, const uint8_t ee )
{
    return(aa || bb || cc || dd || ee);
}