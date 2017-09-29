
// the tricky part is serializing the skipgram class's data member
// to send out to other processes

# include <vector>
# include <string>
# include <utility>
# include <unordered_map>

# include <boost/functional/hash.hpp>

# include <boost/serialization/string.hpp>
# include <boost/serialization/utility.hpp>
# include <boost/serialization/unordered_map.hpp>
# include <boost/serialization/archive_input_unordered_map.hpp>
# include <boost/serialization/boost_unordered_map.hpp>

typedef std::pair< std::string, std::string > tgram;   // "two gram", i.e. 2-skip-2-gram
typedef std::unordered_map< tgram, int, boost::hash< tgram > > counter;

class skipgram {  

  // so the archiver should recognize how to serialize the std::pair 
  // and then the std::string, and then the integer automagically...?
  friend class boost::serialization::access;
  
  template<class Archive>
    void serialize(Archive & ar, const unsigned int version, counter c) {
    for( auto mi=c.begin( ); mi != c.end( ); ++mi ) {
      ar << mi->first << mi->second;
    }
  }
  
  public:
  skipgram( const std::string& fname, int wnd_sz );
  ~skipgram( ) = default;
  // copy
  // move
  // assignment

  void readFile( );
  //void split1( std::string text, const std::string& delims );
  //void readGzip( );

  void readStdin( );
  void split2( const std::string &source );
  void processLine( const std::string& line );
  void writeOut( );
  //private:
  counter c;
  std::string infname;
  int window_size;
  //std::string outfname;
};
