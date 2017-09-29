
// multiple producer / sequential consumer

// start as many threads as files, skipgram each file, write to a synchronized queue; wait until 
// all threads have finished, combine dicts from the queue two at a time until one remains


# include <thread>
# include <future>

# include <queue>
# include <utility>

# include <iostream>

# include "count_dependencies.h"


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

    bool empty( ) {
    std::lock_guard<std::mutex> lock(m_mutex);
    return m_queque.empty( );
  }

  size_t size( ) {
    std::lock_guard<std::mutex> lock(m_mutex);
    return m_queque.size( );
  }

  
  T& front( ) {
    std::lock_guard<std::mutex> lock(m_mutex);
    return m_queque.front( );
  }

private:
  std::queue<T> m_queque;
  mutable std::mutex m_mutex;
};



void dependency_func( const std::string& fname, my_queue< dict >& mq, int window_sz ) {
  skipgram s( fname, window_sz );
  s.readGzip( );
  mq.push( std::move(s.getCounter( ) ) );
}


void aggregate_dicts( dict d1, const dict& d2, my_queue< dict >& mq) {
  for( auto i=d2.begin( ); i != d2.end( ); ++i ) {
    tgram key = std::make_pair( i->first.first, i->first.second );
    auto found = d1.find( key );
    if( found == d1.end( ) ) {
      d1[ key ] = i->second;
    }
    else {
      d1[ key ] += i->second;
    }
  }
  mq.push( d1 );
}


int main( int argc, char** argv ) {

  // generate names of dependecy-parsed files (over-generates)
  std::vector<std::string> filenames;
  const std::string alpha( "abcdefghijk" );
  for( int i=0; i!=2; ++i ) {
    for( auto j=alpha.begin( ); j!=alpha.end( ); ++j ) {
      filenames.push_back("/om/user/ckringen/data/parsing2/en.0" + std::to_string(i) + ".parsed.a" + *j + ".gz");      
    }
  }
    
  int window_sz = atoi(argv[1]);
  std::vector< std::thread > v;
  my_queue< dict > mq;

  for( auto iter=filenames.begin( ); iter!=filenames.end( ); ++iter ) {
    v.push_back( std::thread( dependency_func, *iter, std::ref(mq), window_sz ));
  }
  
  for( auto& th : v ) {
    th.join( );
  }

  while( mq.size( ) >= 2 ) {
    dict d1 = mq.front( );
    mq.pop( );
    const dict& d2 = mq.front( );
    mq.pop( );
    aggregate_dicts( d1, d2, std::ref( mq ) );
  }

  const dict final = mq.front( );
  for( auto i=final.begin( ); i != final.end( ); ++i ) {
    std::cout << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
  }
  
  return 0;
}
