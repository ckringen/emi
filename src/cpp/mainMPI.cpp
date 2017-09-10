
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

  //std::cout << "inside main " << std::endl;

  // set up Boost::MPI 
  mpi::environment env;
  mpi::communicator world;  


  // basic input parameters
  std::string r;  
  std::ostringstream convert;
  convert << world.rank( );

  std::string fname = "/om/user/ckringen/data/commoncrawl_en_deduped_filtered/en.0" + convert.str( ) + ".gz";
  //std::string fname = "sample0" + convert.str( ) + ".txt.gz";
  int window_sz = 2;

  //std::cout << convert.str( ) << " sees " << fname << std::endl;
  
  // count bigrams
  skipgram s( fname, window_sz );
  s.readGzip( );
  counter q;
  
  mpi::reduce(world,
  	      s.c,
  	      q,
  	      combineCounters, 
  	      0);

  std::cout << "finished reducing " << std::endl;
  
  // for( auto i=q.begin( ); i != q.end( ); ++i ) {
  //   std::cout << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
  // }  

  // collate all dictionares together
  if (world.rank() == 0) {    
    std::cout << "inside process 0 " << std::endl;
      // for( auto i=q.begin( ); i != q.end( ); ++i ) {
      // 	std::cout << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
      // }
  }  
  return 0;
}
  
