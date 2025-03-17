> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:**  2.15

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| arrayIndexOutOfBounds | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| arrayIndexOutOfBoundsCond | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| arrayIndexThenCheck | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| autoVariables | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| autovarInvalidDeallocation | 
     MEM34-C. Only free memory allocated dynamically
     |
| bitwiseOnBoolean | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| comparePointers | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| danglingLifetime | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| deallocret | 
     MEM30-C. Do not access freed memory
     |
| deallocuse | 
     MEM30-C. Do not access freed memory
     |
| doubleFree | 
     MEM30-C. Do not access freed memory
     |
| floatConversionOverflow | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| ignoredReturnValue | 
     EXP12-C. Do not ignore values returned by functions
     |
| invalidLengthModifierError | 
     FIO47-C. Use valid format strings
     |
| invalidLifetime | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| invalidscanf | 
     FIO47-C. Use valid format strings
     |
| invalidScanfFormatWidth | 
     FIO47-C. Use valid format strings
     |
| IOWithoutPositioning | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| leakReturnValNotUsed | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| leakReturnValNotUsed | 
     EXP12-C. Do not ignore values returned by functions
     |
| leakUnsafeArgAlloc | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| memleak | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| memleakOnRealloc | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| memsetValueOutOfRange | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| mismatchAllocDealloc | 
     MEM34-C. Only free memory allocated dynamically
     |
| missingReturn | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| negativeArraySize | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| negativeIndex | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| nullPointer | 
     EXP34-C. Do not dereference null pointers
     |
| nullPointerDefaultArg | 
     EXP34-C. Do not dereference null pointers
     |
| nullPointerRedundantCheck | 
     EXP34-C. Do not dereference null pointers
     |
| outOfBounds | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| possibleBufferAccessOutOfBounds | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| preprocessorErrorDirective | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| resourceLeak | 
     FIO42-C. Close files when they are no longer needed
     |
| returnDanglingLifetime | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| shiftNegative | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| shiftTooManyBits | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| suspiciousFloatingPointCast | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| uninitdata | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitMemberVar | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitstring | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitStructMember | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitvar | 
     EXP33-C. Do not read uninitialized memory
     |
| unknownEvaluationOrder | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| wrongPrintfScanfArgNum | 
     FIO47-C. Use valid format strings
     |
| wrongPrintfScanfParameterPositionError | 
     FIO47-C. Use valid format strings
     |
| zerodiv | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| zerodivcond | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |

