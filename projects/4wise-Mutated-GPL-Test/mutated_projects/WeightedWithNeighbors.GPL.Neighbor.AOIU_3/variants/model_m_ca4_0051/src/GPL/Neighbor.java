// This is a mutant program.
// Author : ysma

package GPL; 

import java.util.LinkedList; 


public   class  Neighbor  implements EdgeIfc, NeighborIfc {
	
    public  Vertex neighbor;

	

    // This constructor has to be present here so that the default one
    // Called on Weighted can call it, i.e. it is not longer implicit
    //__feature_mapping__ [UndirectedWithNeighbors] [15:17]
	public Neighbor()  {
        neighbor = null;
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [19:22]
	public Neighbor( Vertex theNeighbor )
   {
        NeighborConstructor( theNeighbor );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [29:32]
	public  void setWeight( int weight )
    {
        this.weight = -weight;
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [34:37]
	public  int getWeight()
    {
        return this.weight;
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [27:29]
	public void NeighborConstructor( Vertex theNeighbor ) {
        neighbor = theNeighbor;
    }

	

     //__feature_mapping__ [UndirectedWithNeighbors] [31:34]
	private void  display__wrappee__UndirectedWithNeighbors()
    {
        System.out.print( neighbor.name + " ," );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [23:27]
	public  void display()
    {
        System.out.print( " Weight = " + weight + " " );
        display__wrappee__UndirectedWithNeighbors();
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [36:36]
	public Vertex getStart( ) { return null; }

	
    //__feature_mapping__ [UndirectedWithNeighbors] [37:37]
	public Vertex getEnd( ) { return null; }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [39:42]
	public Vertex getOtherVertex( Vertex vertex )
    {
        return neighbor;
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [44:46]
	public void adjustAdorns( EdgeIfc the_edge )
    {
    }

	

    public int weight;

	

    //__feature_mapping__ [WeightedWithNeighbors] [12:15]
	public Neighbor( Vertex theNeighbor, int theWeight )
    {
        NeighborConstructor( theNeighbor, theWeight );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [17:21]
	public  void NeighborConstructor( Vertex theNeighbor, int theWeight )
    {
        NeighborConstructor( theNeighbor );
        weight = theWeight;
    }


}
