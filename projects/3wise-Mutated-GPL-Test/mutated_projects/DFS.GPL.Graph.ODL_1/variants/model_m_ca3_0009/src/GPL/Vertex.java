package GPL; 
import java.util.LinkedList; 
import java.util.Iterator; 

import java.lang.Integer; 
import java.util.Collections; 
import java.util.Comparator; 

public   class  Vertex {
	
    public LinkedList adjacentNeighbors;

	
    public String name;

	

    //__feature_mapping__ [UndirectedWithNeighbors] [13:16]
	public Vertex() 
    {
        VertexConstructor();
    }

	
      
     //__feature_mapping__ [UndirectedWithNeighbors] [18:22]
	private void  VertexConstructor__wrappee__UndirectedWithNeighbors() 
    {
        name      = null;
        adjacentNeighbors = new LinkedList();
    }

	

    //__feature_mapping__ [DFS] [9:13]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__UndirectedWithNeighbors( );
        visited = false;
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [24:28]
	public  Vertex assignName( String name ) 
    {
        this.name = name;
        return ( Vertex ) this;
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [30:33]
	public String getName( )
    {
        return this.name;
    }

	
    
    //__feature_mapping__ [UndirectedWithNeighbors] [35:38]
	public LinkedList getNeighborsObj( )
    {
 	  return adjacentNeighbors;
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [40:54]
	public VertexIter getNeighbors( )
    {
        return new VertexIter( )
        {
            private Iterator iter = adjacentNeighbors.iterator( );
            public Vertex next( ) 
            { 
                return ( ( Neighbor )iter.next( ) ).neighbor; 
            }
            public boolean hasNext( ) 
            { 
                return iter.hasNext( ); 
            }
        };
    }

	

     //__feature_mapping__ [UndirectedWithNeighbors] [56:66]
	private void  display__wrappee__UndirectedWithNeighbors( ) 
    {
        System.out.print( "Node " + name + " connected to: " );

        for ( VertexIter vxiter = getNeighbors( ); vxiter.hasNext( ); )
        {
            System.out.print( vxiter.next( ).getName( ) + ", " );
        }

        System.out.println();
    }

	 // weight so far from s to it
            
     //__feature_mapping__ [MSTPrim] [14:18]
	private void  display__wrappee__MSTPrim( ) 
    {
        System.out.print( " Pred " + pred + " Key " + key + " " );
        display__wrappee__UndirectedWithNeighbors( );
    }

	 // of dftNodeSearch

     //__feature_mapping__ [DFS] [47:53]
	private void  display__wrappee__DFS( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__MSTPrim( );
    }

	
    
    //__feature_mapping__ [WeightedWithNeighbors] [20:23]
	public void display()
    {
        display__wrappee__DFS();
    }

	
//--------------------
// differences
//--------------------

    //__feature_mapping__ [UndirectedWithNeighbors] [71:74]
	public void addEdge( Neighbor n ) 
    {
        adjacentNeighbors.add( n );
    }

	

     //__feature_mapping__ [UndirectedWithNeighbors] [76:78]
	private void  adjustAdorns__wrappee__UndirectedWithNeighbors( Neighbor sourceNeighbor )
    {
    }

	
    
    //__feature_mapping__ [WeightedWithNeighbors] [12:18]
	public void adjustAdorns( Neighbor sourceNeighbor )
     {
        Neighbor targetNeighbor = 
                ( Neighbor )adjacentNeighbors.getLast();
        targetNeighbor.weight = sourceNeighbor.weight;
        adjustAdorns__wrappee__UndirectedWithNeighbors( sourceNeighbor );
    }

	

    //__feature_mapping__ [UndirectedWithNeighbors] [80:96]
	public EdgeIter getEdges( )
    {
        return new EdgeIter( )
        {
            private Iterator iter = adjacentNeighbors.iterator( );
            public EdgeIfc next( ) 
            { 
                return ( Neighbor ) iter.next( ); 

//              return ( ( EdgeIfc ) ( ( Neighbor )iter.next( ) ).edge );
            }
            public boolean hasNext( ) 
            { 
              return iter.hasNext( ); 
            }
        };
    }

	
    public String pred;

	 // the predecessor vertex if any
    public int key;

	
    public boolean visited;

	

    //__feature_mapping__ [DFS] [15:19]
	public void init_vertex( WorkSpace w ) 
    {
        visited = false;
        w.init_vertex( ( Vertex ) this );
    }

	

    //__feature_mapping__ [DFS] [21:45]
	public void nodeSearch( WorkSpace w ) 
    {
        Vertex v;

        // Step 1: Do preVisitAction.
        //            If we've already visited this node return
        w.preVisitAction( ( Vertex ) this );

        if ( visited )
            return;

        // Step 2: else remember that we've visited and
        //         visit all neighbors
        visited = true;

        for ( VertexIter  vxiter = getNeighbors(); vxiter.hasNext(); ) 
        {
            v = vxiter.next( );
            w.checkNeighborAction( ( Vertex ) this, v );
            v.nodeSearch( w );
        }

        // Step 3: do postVisitAction now
        w.postVisitAction( ( Vertex ) this );
    }

	
    //__feature_mapping__ [WeightedWithNeighbors] [4:10]
	public void addWeight( Vertex end, int theWeight ) 
    {
        Neighbor the_neighbor = 
                ( Neighbor ) ( end.adjacentNeighbors ).removeLast();
        the_neighbor.weight = theWeight;
        ( end.adjacentNeighbors ).add( the_neighbor );
    }


}
