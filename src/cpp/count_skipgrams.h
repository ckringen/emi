
# include <vector>
# include <utility>
# include <string>
# include <unordered_map>

// need to provide a custom hash for using tgram as a key
#include <boost/functional/hash.hpp>

typedef std::pair< std::string, std::string > tgram;   // "two gram", i.e. 2-skip-2-gram


class skipgram {  
 public:
  skipgram( std::string fname, int wnd_sz );
  ~skipgram( ) = default;
  // copy
  // move
  // assignment

  void readFile( );
  void readStdin( );
  void readGzip( );
  void processLine( std::string line );
  void writeOut( );

private:
  std::unordered_map< tgram, int, boost::hash< tgram > > counter;
  std::string infname;
  std::string outfname;
  int window_size;
};



