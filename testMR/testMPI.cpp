
# include <mpi.h>
# include <stdio.h>

int main( int argc, char** argv ) {

  MPI_Init( NULL, NULL );

  int world_size, world_rank, name_len;
  MPI_Comm_size( MPI_COMM_WORLD, &world_size );
  MPI_Comm_rank( MPI_COMM_WORLD, &world_rank );

  char processor_name[ MPI_MAX_PROCESSOR_NAME ];
  MPI_Get_processor_name( processor_name, &name_len);

  printf("Hello wold from processor %s, rank %d, out of %d processors\n",
	 processor_name, world_rank, world_size );

  MPI_Finalize( );
}

		 
