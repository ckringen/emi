
// process ascii dependency output (parsey mcparseface) or plain text output
// pull out n-skip-2-grams from both, stick in dictionary object

# include <vector>
# include <string>
# include <utility>
# include <unordered_map>

#include <boost/functional/hash.hpp>

typedef std::pair< std::string, std::string > tgram;   
typedef std::unordered_map< tgram, int, boost::hash< tgram > > dict;


class skipgram {  
 public:
  skipgram( const std::string& fname, int wnd_sz );
  ~skipgram( ) = default;
   
  void readGzip( );  
  void processDependency( const std::vector<std::vector<std::string>>& line );
  dict getCounter( );
  
 private:
  std::unordered_map< tgram, int, boost::hash< tgram > > counter;
  std::string infname;
  int window_size;
};



