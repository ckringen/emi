
# include <boost/mpi/environment.hpp>
# include <boost/mpi/communicator.hpp>
# include <iostream>

namespace mpi = boost::mpi;

int main( int argc, char** argv ) {

  mpi::environment env;
  mpi::communicator world;
  std::cout << "process " << world.rank( ) << " of " << world.size( ) << '\n';
  

  return 0;
}
