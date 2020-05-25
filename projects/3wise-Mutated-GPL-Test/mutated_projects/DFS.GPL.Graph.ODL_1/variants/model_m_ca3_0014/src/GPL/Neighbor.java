package GPL; 

import java.util.LinkedList; 

// end of Vertex class
 
  // *************************************************************************
  
public   class  Neighbor  implements EdgeIfc, NeighborIfc {
	
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
	private void  display__wrappee__DirectedWithNeighbors () 
    {
        System.out.print( neighbor.name + " ," );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [20:24]
	public void display()
    {
        System.out.print( " Weight = " + weight + " " );
        display__wrappee__DirectedWithNeighbors();
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

	

    //__feature_mapping__ [WeightedWithNeighbors] [26:29]
	public void setWeight(int weight)
    {
        this.weight = weight;
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

	
    public int weight;

	

    //__feature_mapping__ [WeightedWithNeighbors] [10:12]
	public Neighbor( Vertex theNeighbor, int theWeight ) {
        NeighborConstructor( theNeighbor, theWeight );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [14:18]
	public void NeighborConstructor( Vertex theNeighbor, int theWeight )
    {
        NeighborConstructor( theNeighbor );
        weight = theWeight;
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [31:34]
	public int getWeight()
    {
        return this.weight;
    }


}
