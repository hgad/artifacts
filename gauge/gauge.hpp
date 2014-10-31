////////////////////////////////////////////////////////////////////////////////
//                                                                            //
// Copyright (c) 2014, Haitham Gad                                            //
// All rights reserved.                                                       //
//                                                                            //
// Redistribution and use in source and binary forms, with or without         //
// modification, are permitted provided that the following conditions are     //
// met:                                                                       //
//                                                                            //
// 1. Redistributions of source code must retain the above copyright notice,  //
//    this list of conditions and the following disclaimer.                   //
//                                                                            //
// 2. Redistributions in binary form must reproduce the above copyright       //
//    notice, this list of conditions and the following disclaimer in the     //
//    documentation and/or other materials provided with the distribution.    //
//                                                                            //
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS        //
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED  //
// TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR //
// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR           //
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,      //
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,        //
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR         //
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF     //
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING       //
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS         //
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.               //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////

#pragma once

#include <iostream>
#include <boost/noncopyable.hpp>
#include <boost/timer/timer.hpp>

namespace gauge {

inline void report_time(const char *tool, double cpu_time, double wall_time) {
  std::cout << tool << ": [[ cpu = " << cpu_time / 1e9
            << " sec, wall = " << wall_time / 1e9 << " sec ]]" << std::endl;
}

class timer : public boost::noncopyable {
  public:
    timer() {}

    ~timer() {
      boost::timer::cpu_times dur = d_timer.elapsed();
      report_time("timer", dur.user + dur.system, dur.wall);
    }

  private:
    boost::timer::cpu_timer d_timer;
};

class profiler : public boost::noncopyable {
  public:
    profiler() {}

    ~profiler() {
      boost::timer::cpu_times dur = d_timer.elapsed();
      cpu_time() += (dur.user + dur.system);
      wall_time() += dur.wall;
    }

    static void reset() {
      cpu_time() = 0.0;
      wall_time() = 0.0;
    }

    static void report() {
      report_time("profiler", cpu_time(), wall_time());
    }

    static double &cpu_time() {
      static double s_cpu_time = 0.0;
      return s_cpu_time;
    }

    static double &wall_time() {
      static double s_wall_time = 0.0;
      return s_wall_time;
    }

  private:
    boost::timer::cpu_timer d_timer;
};

}

