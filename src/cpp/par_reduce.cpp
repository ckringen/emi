
# include <utility>
# include <iostream>
# include <queue>

# include <thread>
# include <condition_variable>
# include <mutex>

# include "count_skipgrams.h"

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


void skipgram_func( int i, my_queue<int>& mq ) {
  // std::string fname = "/home/aik/PersonalProjects/Languages/C++/threading/data/testfile" + std::to_string(i) + ".txt";
  // int window_sz = 2;   
  // skipgram s( fname, window_sz );
  // s.readFile( );
  //mq.push( s.getCounter( ) );
  std::cout << "adding " << std::to_string(i) << '\n';
  mq.push( i );
}

void aggregate_dicts( my_queue< dict >& mq) {
  
  while( mq.size( ) >= 2 ) {
    std::cout << "Aggregating!\n";
    dict d1 = mq.front( );
    const dict& d2 = mq.front( );
    
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
}

void aggregate_parallel( my_queue< int >& mq ) {
  int i1( mq.front( ) );
  mq.pop( );
  int i2( mq.front( ) );
  mq.pop( );
  std::cout << "popping: " << std::to_string(i1) << ' ' << std::to_string(i2) << " pushing: " << std::to_string(i1 + i2) << '\n';
  mq.push( i1 + i2 );
}

void aggregate_ints( my_queue< int >& mq ) {
  std::cout << "|Q| = " << mq.size( ) << '\n';
  while( mq.size( ) >= 2 ) {
    int i1( mq.front( ) );
    mq.pop( );
    int i2( mq.front( ) );
    mq.pop( );
    std::cout << "popping: " << std::to_string(i1) << ' ' << std::to_string(i2) << "pushing: " << std::to_string(i1 + i2) << '\n';
    mq.push( i1 + i2 );
  }
}

int main( int argc, char** argv ) {

  my_queue<int> mq;
  
  for( int i=0; i!=15; ++i ) {
    
    // do a block of work in parallel; wait for them to finish
    std::thread s1(skipgram_func, i, std::ref(mq) );
    std::thread s2(skipgram_func, i+1, std::ref(mq) );
    std::thread s3(skipgram_func, i+2, std::ref(mq) );
    s1.join( ); s2.join( ); s3.join( );

    std::cout << "|Q| = " << mq.size( ) << '\n';
  
    // // reduce current work down to a single value; wait to finish
    // std::thread r(aggregate_ints, std::ref(mq) );    
    // r.join( );

    // // reduce in parallel with multiple threads
    std::thread r1(aggregate_parallel, std::ref(mq) );
    std::thread r2(aggregate_parallel, std::ref(mq) ); 
    r1.join( ); r2.join( );
  }

  std::cout << "done\n";
  while(!mq.empty( ) ) {
    std::cout << std::to_string(mq.front( ) )<< '\n';
    mq.pop( );
  }
return 0;
}
