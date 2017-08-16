
# include <string>

# include "count_skipgrams.h"

int main( int argc, char** argv ) {  
  std::string fname = argv[1];
  int window_sz = atoi(argv[2]);
  
  skipgram s( fname, window_sz );
  s.readFile( );
  s.writeOut( );
  
  return 0;
}
