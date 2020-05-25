package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 
import java.util.Collections; 
import java.util.Comparator; 

  // *************************************************************************

public   class  Vertex {
	
    public LinkedList adjacentNeighbors;

	
    public String name;

	
   
    //__feature_mapping__ [DirectedWithNeighbors] [13:15]
	public Vertex() {
        VertexConstructor();
    }

	
    //__feature_mapping__ [DirectedWithNeighbors] [16:19]
	public String getName( ) 
    { 
        return name; 
    }

	

     //__feature_mapping__ [DirectedWithNeighbors] [21:24]
	private void  VertexConstructor__wrappee__DirectedWithNeighbors() {
        name      = null;
        adjacentNeighbors = new LinkedList();
    }

	

    //__feature_mapping__ [DFS] [9:13]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__DirectedWithNeighbors( );
        visited = false;
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [26:29]
	public  Vertex assignName( String name ) {
        this.name = name;
        return ( Vertex ) this;
    }

	
   
    //__feature_mapping__ [DirectedWithNeighbors] [31:33]
	public void addEdge( Neighbor n ) {
        adjacentNeighbors.add( n );
    }

	


    //__feature_mapping__ [DirectedWithNeighbors] [36:51]
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

	

    //__feature_mapping__ [DirectedWithNeighbors] [53:54]
	public void adjustAdorns( Neighbor sourceNeighbor )
      {}

	
      
     //__feature_mapping__ [DirectedWithNeighbors] [56:66]
	private void  display__wrappee__DirectedWithNeighbors() 
    {
        System.out.print( "Node " + getName( ) + " connected to: " );

        for(VertexIter vxiter = getNeighbors( ); vxiter.hasNext( ); )
         {
            Vertex v = vxiter.next( );
            System.out.print( v.getName( ) + ", " );
        }
        System.out.println( );
    }

	

     //__feature_mapping__ [Number] [12:16]
	private  void  display__wrappee__Number()
    {
        System.out.print( " # " + ++VertexNumber + " " );
        display__wrappee__DirectedWithNeighbors();
    }

	
      
     //__feature_mapping__ [StronglyConnected] [15:19]
	private void  display__wrappee__StronglyConnected() {
        System.out.print( " FinishTime -> " + finishTime + " SCCNo -> " 
                        + strongComponentNumber );
        display__wrappee__Number();
    }

	 // of dftNodeSearch

    //__feature_mapping__ [DFS] [47:53]
	public void display( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__StronglyConnected( );
    }

	

    public int VertexNumber;

	
    public int finishTime;

	
    public int strongComponentNumber;

	
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
