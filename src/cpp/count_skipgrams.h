
# include <vector>
# include <string>
# include <utility>
# include <unordered_map>

// need to provide a custom hash for using tgram as a key
#include <boost/functional/hash.hpp>

typedef std::pair< std::string, std::string > tgram;   // "two gram", i.e. 2-skip-2-gram


class skipgram {  
 public:
  skipgram( const std::string& fname, int wnd_sz );
  ~skipgram( ) = default;
  // copy
  // move
  // assignment
  
  //void readFile( );
  //void split1( std::string text, const std::string& delims );
  //void readGzip( );
  
  void readStdin( );
  void split2( const std::string &source );
  void processLine( const std::string& line );
  void writeOut( );

private:
  std::unordered_map< tgram, int, boost::hash< tgram > > counter;
  std::string infname;
  int window_size;
  //std::string outfname;
};



