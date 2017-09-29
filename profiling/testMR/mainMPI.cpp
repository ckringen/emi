
# include <algorithm>
# include <functional>
# include <string>

# include <sstream>
# include <iostream>
# include <fstream>

# include <boost/mpi.hpp>

# include "count_skipgrams.h"

namespace mpi = boost::mpi;

int main( int argc, char** argv ) {  

  // set up Boost::MPI 
  mpi::environment env;
  mpi::communicator world;  


  // basic input parameters
  std::string r;  
  std::ostringstream convert;
  convert << world.rank( );
  std::string fname = "/home/ckringen/emi/testMR/testfile" + convert.str( ) + ".txt";
  int window_sz = 2;


  // count bigrams
  skipgram s( fname, window_sz );
  s.readFile( );


  // collate all dictionares together
  if (world.rank() == 0) {    
    std::vector< counter > q;
    mpi::gather( world, s.c, q, 0 );

    for( auto i=q.begin( ); i != q.end( ); ++i ) {
      std::cout << "dictionary #" << std::distance(i,q.end( ) ) << std::endl;

      for( auto j=i->begin( ); j!=i->end( ); ++j ) {
	std::cout << j->first.first << ' ' << j->first.second << '\t' << j->second << '\n';
      }
    }
  }

  // pass your data to the root
  else {
    mpi::gather( world, s.c, 0 );
  }
  
  return 0;
  
}
  
