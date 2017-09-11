
// so we need to find a way to store the computed skipgram dictionaries

# include <thread>
# include <future>

# include <queue>
# include <utility>

# include <sstream>
# include <iostream>

# include "count_skipgrams.h"

// stash computed dictionaries here
template<typename T>
class my_queue {
public:
  void push( const T& value ) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_queque.push(value);
  }
  
  void pop() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_queque.pop();
  }

  void showSizes( ) {
    while( !m_queque.empty( ) ) {      
      std::cout << m_queque.front( ).size( ) << std::endl;
      m_queque.pop( );
    }
  }
  
private:
  std::queue<T> m_queque;
  mutable std::mutex m_mutex;
};


// should modify shared state by storing skipgram dicts
void skipgram_func( int i, my_queue< dict >& mq ) {
  // count skipgrams object
  std::string number;  
  std::ostringstream convert;
  convert << i;

  std::string fname = "/home/aik/PersonalProjects/Languages/C++/threading/data/testfile" + convert.str( ) + ".txt";
  int window_sz = 2;
  
  skipgram s( fname, window_sz );
  s.readFile( );

  // I think I want to move this into the q; which means I need to write a move constructor!
  mq.push( std::move(s.getCounter( ) ) );
}

int main( int argv, char** argc ) {

  std::vector< std::thread > v;
  my_queue< dict > mq;

  
  // start a bunch of threads to skipgram a bunch of files
  for( int i = 1; i!=3; ++i ) {
    v.push_back( std::thread( skipgram_func, i, std::ref(mq) ));
  }
  
  // join the threads
  for( auto& th : v ) {
    th.join( );
  }

  // prove shared state exists
  mq.showSizes( );

  // recursively reduce multiple counters into one


  return 0;
}
