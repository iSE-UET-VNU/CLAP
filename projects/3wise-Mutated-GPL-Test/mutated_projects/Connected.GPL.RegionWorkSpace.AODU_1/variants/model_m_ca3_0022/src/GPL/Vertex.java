package GPL; 

import java.util.LinkedList; 
import java.util.Iterator; 

  // *************************************************************************

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

	

     //__feature_mapping__ [Number] [9:13]
	private void  display__wrappee__Number( ) 
    {
        System.out.print( " # "+ VertexNumber + " " );
        display__wrappee__UndirectedWithNeighbors( );
    }

	 // of dftNodeSearch

    //__feature_mapping__ [DFS] [47:53]
	public void display( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__Number( );
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
	public void adjustAdorns( Neighbor sourceNeighbor )
    {
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

	
    public int VertexNumber;

	
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


}
