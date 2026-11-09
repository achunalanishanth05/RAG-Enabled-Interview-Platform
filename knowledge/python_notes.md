# Python Interview Notes

## Lists vs Tuples
- Lists are mutable (can be changed). Tuples are immutable.
- Tuples are slightly faster and can be used as dictionary keys.
- Use a list when data changes, a tuple when it should stay fixed.

## Decorators
- A decorator is a function that wraps another function to add behavior.
- It is applied with the @ symbol above a function definition.
- Common uses: logging, timing, authentication.

## Generators
- A generator uses `yield` instead of `return`.
- It produces values one at a time, so it saves memory on large data.
- Generators are lazy: values are computed only when requested.

## The GIL
- The Global Interpreter Lock lets only one thread run Python bytecode at a time.
- It limits CPU-bound multithreading.
- Use multiprocessing for CPU-bound work, and threading or asyncio for I/O-bound work.

## Mutable Default Arguments
- Default values are created once, when the function is defined.
- `def f(x=[])` shares the same list across calls, a common bug.
- Fix: use `x=None` and create the list inside the function.