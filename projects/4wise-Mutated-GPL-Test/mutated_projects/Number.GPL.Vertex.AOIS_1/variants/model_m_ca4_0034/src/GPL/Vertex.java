package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 

// *************************************************************************

public   class  Vertex  implements EdgeIfc, NeighborIfc {
	
    public LinkedList adjacentVertices;

	
    public String name;

	

    //__feature_mapping__ [UndirectedOnlyVertices] [13:16]
	public Vertex( )
    {
        VertexConstructor( );
    }

	

     //__feature_mapping__ [UndirectedOnlyVertices] [18:22]
	private void  VertexConstructor__wrappee__UndirectedOnlyVertices( )
    {
        name      = null;
        adjacentVertices = new LinkedList();
    }

	

    //__feature_mapping__ [BFS] [11:15]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__UndirectedOnlyVertices();
        visited = false;
    }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [24:28]
	public  Vertex assignName( String name )
    {
        this.name = name;
        return ( Vertex ) this;
    }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [30:45]
	public VertexIter getNeighbors( )
    {
        return new VertexIter( )
        {
            private Iterator iter = adjacentVertices.iterator( );
            public Vertex next( )
            {
               return ( Vertex )iter.next( );
            }

            public boolean hasNext( )
            {
               return iter.hasNext( );
            }
        };
    }

	

     //__feature_mapping__ [UndirectedOnlyVertices] [47:56]
	private void  display__wrappee__UndirectedOnlyVertices() {
        int s = adjacentVertices.size();
        int i;

        System.out.print( "Vertex " + name + " connected to: " );
        for ( i=0; i<s; i++ )
            System.out.print( ( ( Vertex ) adjacentVertices.get( i ) ).name
                                                + ", " );
        System.out.println();
    }

	

     //__feature_mapping__ [Number] [12:16]
	private  void  display__wrappee__Number()
    {
        System.out.print( " # " + ++VertexNumber + " " );
        display__wrappee__UndirectedOnlyVertices();
    }

	

     //__feature_mapping__ [Connected] [9:13]
	private void  display__wrappee__Connected( ) 
    {
        System.out.print( " comp# "+ componentNumber + " " );
        display__wrappee__Number( );
    }

	 // of bfsNodeSearch

    //__feature_mapping__ [BFS] [69:76]
	public void display( ) 
    {
        if ( visited )
            System.out.print( "  visited " );
        else
            System.out.println( " !visited " );
        display__wrappee__Connected( );
    }

	
//--------------------
// differences
//--------------------

    //__feature_mapping__ [UndirectedOnlyVertices] [61:63]
	public void addAdjacent( Vertex n ) {
        adjacentVertices.add( n );
    }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [65:66]
	public void adjustAdorns( Vertex the_vertex, int index )
      {}

	
    //__feature_mapping__ [UndirectedOnlyVertices] [67:70]
	public LinkedList getNeighborsObj( )
    {
      return adjacentVertices;
    }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [72:88]
	public EdgeIter getEdges( )
    {
        return new EdgeIter( )
        {
            private Iterator iter = adjacentVertices.iterator( );
            public EdgeIfc next( )
            {
                return ( EdgeIfc ) iter.next( );

//              return ( ( EdgeIfc ) ( ( Neighbor )iter.next( ) ).edge );
            }
            public boolean hasNext( )
            {
              return iter.hasNext( );
            }
        };
    }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [90:93]
	public String getName( )
    {
        return this.name;
    }

	

//--------------------
// from EdgeIfc
//--------------------

    //__feature_mapping__ [UndirectedOnlyVertices] [99:99]
	public Vertex getStart( ) { return null; }

	
    //__feature_mapping__ [UndirectedOnlyVertices] [100:100]
	public Vertex getEnd( ) { return null; }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [102:102]
	public void setWeight( int weight ){}

	
    //__feature_mapping__ [UndirectedOnlyVertices] [103:103]
	public int getWeight() { return 0; }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [105:108]
	public Vertex getOtherVertex( Vertex vertex )
    {
        return this;
    }

	



    //__feature_mapping__ [UndirectedOnlyVertices] [112:114]
	public void adjustAdorns( EdgeIfc the_edge )
    {
    }

	

    public int VertexNumber;

	
    public int componentNumber;

	
    public boolean visited;

	

    //__feature_mapping__ [BFS] [17:21]
	public void init_vertex( WorkSpace w ) 
    {
        visited = false;
        w.init_vertex( ( Vertex ) this );
    }

	

    //__feature_mapping__ [BFS] [23:67]
	public void nodeSearch( WorkSpace w ) 
    {
        int     s, c;
        Vertex  v;
        Vertex  header;

        // Step 1: if preVisitAction is true or if we've already
        //         visited this node
        w.preVisitAction( ( Vertex ) this );

        if ( visited )
        {
            return;
        }

        // Step 2: Mark as visited, put the unvisited neighbors in the queue
        //     and make the recursive call on the first element of the queue
        //     if there is such if not you are done
        visited = true;

        // Step 3: do postVisitAction now, you are no longer going through the
        // node again, mark it as black
        w.postVisitAction( ( Vertex ) this );

        // enqueues the vertices not visited
        for ( VertexIter vxiter = getNeighbors( ); vxiter.hasNext( ); )
        {
            v = vxiter.next( );

            // if your neighbor has not been visited then enqueue
            if ( !v.visited ) 
            {
                GlobalVarsWrapper.Queue.add( v );
            }

        } // end of for

        // while there is something in the queue
        while( GlobalVarsWrapper.Queue.size( )!= 0 )
        {
            header = ( Vertex ) GlobalVarsWrapper.Queue.get( 0 );
            GlobalVarsWrapper.Queue.remove( 0 );
            header.nodeSearch( w );
        }
    }


}
