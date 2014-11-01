Gauge: A Time Profiler
====================

Gauge is a tiny single-header-file library to quickly measure CPU and Wall-Clock
time of code sections. It provides two classes:

1. `gauge::timer`: Measures the time spent in a code section when executed once.
2. `gauge::profiler`: Measures the accumulative time spent in a code section
   over the entire (or partial) lifetime of the program.

`gauge::timer` dumps its report in the destructor, so to measure the time spent
in a code snippet, first wrap it in braces {}.

`gauge::profiler` reports the time only when you call `profiler::report()`. You
should call this method when all the instances of your code section that you're
interested in have been executed. To reset the profiler time, call
`profiler::reset()`.


Example
-------

This example uses gauge to measure the time spent in every call to test(),
reports the profiler's accumulative time, resets the profiler and does the same
for test2():

    #include "gauge.hpp"

    using namespace gauge;

    void test() {
      // ...

      {
        profiler pf;
        timer tm;

        for (long i = 0; i < 1000000000; ++i);
      } // gauge::timer reports time here

      // ...
    }

    void test2() {
      profiler pf;
      timer tm;

      for (long i = 0; i < 1000000000; ++i);
    }

    int main() {
      for (int i = 0; i < 10; ++i)
        test();

      profiler::report();

      profiler::reset();
      test2();

      profiler::report();
    }

To compile this code, run the following command:

    c++ file.cpp -I/path/to/boost/headers -L/path/to/boost/libs \
                 -lboost_timer-mt -lboost_system-mt

The output on my machine looks like this:

    timer: [[ cpu = 2.43 sec, wall = 2.49487 sec ]]
    timer: [[ cpu = 2.47 sec, wall = 2.49744 sec ]]
    timer: [[ cpu = 2.4 sec, wall = 2.45963 sec ]]
    timer: [[ cpu = 2.34 sec, wall = 2.37833 sec ]]
    timer: [[ cpu = 2.35 sec, wall = 2.34716 sec ]]
    timer: [[ cpu = 2.36 sec, wall = 2.35785 sec ]]
    timer: [[ cpu = 2.35 sec, wall = 2.36559 sec ]]
    timer: [[ cpu = 2.33 sec, wall = 2.33215 sec ]]
    timer: [[ cpu = 2.33 sec, wall = 2.33157 sec ]]
    timer: [[ cpu = 2.33 sec, wall = 2.35699 sec ]]
    profiler: [[ cpu = 23.69 sec, wall = 23.9221 sec ]]
    timer: [[ cpu = 2.36 sec, wall = 2.37659 sec ]]
    profiler: [[ cpu = 2.36 sec, wall = 2.37688 sec ]]


