package GPL; 

import java.util.LinkedList; 

// Vertex class

 // *************************************************************************

public  class  Neighbor  implements EdgeIfc, NeighborIfc {
	
    public  Vertex neighbor;

	

    // This constructor has to be present here so that the default one
    // Called on Weighted can call it, i.e. it is not longer implicit
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Neighbor()  {
        neighbor = null;
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Neighbor( Vertex theNeighbor )
   {
        NeighborConstructor( theNeighbor );
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void setWeight(int weight) {}

	
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public int getWeight() { return 0; }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void NeighborConstructor( Vertex theNeighbor ) {
        neighbor = theNeighbor;
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void display()
    {
        System.out.print( neighbor.name + " ," );
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Vertex getStart( ) { return null; }

	
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Vertex getEnd( ) { return null; }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Vertex getOtherVertex( Vertex vertex )
    {
        return neighbor;
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void adjustAdorns( EdgeIfc the_edge )
    {
    }


}
