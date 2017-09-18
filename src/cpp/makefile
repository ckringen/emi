
# build some things for great good

CPP = g++

FLAGS = -std=c++11 -O3
INCLUDE_PATH = -I/om/user/ckringen/thirdparty/boost-materials/boost_1_65_0
LIB_PATH = -L/om/user/ckringen/thirdparty/boost-materials/boost_1_65_0/stage/lib -L/om/user/ckringen/thirdparty/zlib-materials/zlib-1.2.11
libs = -lpthread -lboost_iostreams -lz


# mainMPI: mainMPI.o count_skipgrams.o
# 	$(MPICC) $(FLAGS) mainMPI.o count_skipgrams.o $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o mainMPI


# older
thread: count_skipgrams2.o main_thread.o
	$(CPP) $(FLAGS) $(INCLUDE_PATH) main_thread.o count_skipgrams2.o $(LIB_PATH) $(libs) -o main_thread

count_skipgrams2.o: count_skipgrams.cpp count_skipgrams.h
	$(CPP) $(FLAGS) $(INCLUDE_PATH) -c count_skipgrams.cpp $(LIB_PATH) $(libs) -o count_skipgrams2.o

main_thread.o: main_thread.cpp
	$(CPP) $(FLAGS) $(INCLUDE_PATH) -c main_thread.cpp $(LIB_PATH) $(libs) -o main_thread.o

clean:
	$(RM) *.o $(bin) testBoost mainMPI main_thread cs count_skipgrams

