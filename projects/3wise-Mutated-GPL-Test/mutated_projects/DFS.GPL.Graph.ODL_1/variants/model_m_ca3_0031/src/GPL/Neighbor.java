package GPL; 

import java.util.LinkedList; 

// *************************************************************************
   
public  class  Neighbor  implements EdgeIfc, NeighborIfc {
	
    public  Vertex neighbor;

	
        
    // This constructor has to be present here so that the default one
    // Called on Weighted can call it, i.e. it is not longer implicit    
    //__feature_mapping__ [DirectedWithNeighbors] [13:16]
	public Neighbor( )
    {
        neighbor = null;
    }

	
    
    //__feature_mapping__ [DirectedWithNeighbors] [18:21]
	public Neighbor( Vertex theNeighbor ) 
    {
        NeighborConstructor( theNeighbor );
    }

	
    
    //__feature_mapping__ [DirectedWithNeighbors] [23:26]
	public void NeighborConstructor( Vertex theNeighbor ) 
    {
        neighbor = theNeighbor;
    }

	
  
    //__feature_mapping__ [DirectedWithNeighbors] [28:31]
	public void display () 
    {
        System.out.print( neighbor.name + " ," );
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [33:36]
	public Vertex getStart( ) 
    { 
       return null; 
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [38:41]
	public Vertex getEnd( ) 
    { 
      return neighbor; 
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [43:45]
	public void setWeight( int weight ) 
    {
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [47:50]
	public Vertex getOtherVertex( Vertex vertex )
    {
        return neighbor;
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [52:54]
	public void adjustAdorns( EdgeIfc the_edge )
    {
    }


}
