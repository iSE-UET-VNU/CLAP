package GPL; 

// dja - trying to fix compile problems
import java.util.Iterator; 

import java.util.LinkedList; 

// *************************************************************************

public   class  Vertex  implements EdgeIfc, NeighborIfc {
	
    public LinkedList adjacentVertices;

	
    public String name;

	
 
    //__feature_mapping__ [DirectedOnlyVertices] [14:16]
	public Vertex() {
        VertexConstructor();
    }

	
  
     //__feature_mapping__ [DirectedOnlyVertices] [18:21]
	private void  VertexConstructor__wrappee__DirectedOnlyVertices() {
        name      = null;
        adjacentVertices = new LinkedList();
    }

	

    //__feature_mapping__ [BFS] [11:15]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__DirectedOnlyVertices();
        visited = false;
    }

	

    //__feature_mapping__ [DirectedOnlyVertices] [23:26]
	public  Vertex assignName( String name ) {
        this.name = name;
        return ( Vertex ) this;
    }

	

    //dja: fix for compile errors during performance improvements
    //__feature_mapping__ [DirectedOnlyVertices] [29:32]
	public String getName( ) 
    { 
        return name; 
    }

	

 
    //__feature_mapping__ [DirectedOnlyVertices] [35:37]
	public void addAdjacent( Vertex n ) {
        adjacentVertices.add( n );
    }

	

    //__feature_mapping__ [DirectedOnlyVertices] [39:40]
	public void adjustAdorns( Vertex the_vertex, int index ) 
      {}

	
      
    // dja - trying to fix compile errors
    //__feature_mapping__ [DirectedOnlyVertices] [43:58]
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

	


     //__feature_mapping__ [DirectedOnlyVertices] [61:70]
	private void  display__wrappee__DirectedOnlyVertices() {
        int s = adjacentVertices.size();
        int i;

        System.out.print( "Vertex " + name + " connected to: " );

        for ( i=0; i<s; i++ )
            System.out.print( ( ( Vertex )adjacentVertices.get( i ) ).name+", " );
        System.out.println();
    }

	

     //__feature_mapping__ [Number] [9:13]
	private void  display__wrappee__Number( ) 
    {
        System.out.print( " # "+ VertexNumber + " " );
        display__wrappee__DirectedOnlyVertices( );
    }

	 // of bfsNodeSearch

    //__feature_mapping__ [BFS] [69:76]
	public void display( ) 
    {
        if ( visited )
            System.out.print( "  visited " );
        else
            System.out.println( " !visited " );
        display__wrappee__Number( );
    }

	

//--------------------
// from EdgeIfc
//--------------------

    //__feature_mapping__ [DirectedOnlyVertices] [76:76]
	public Vertex getStart( ) { return null; }

	
    //__feature_mapping__ [DirectedOnlyVertices] [77:77]
	public Vertex getEnd( ) { return null; }

	

    //__feature_mapping__ [DirectedOnlyVertices] [79:79]
	public void setWeight( int weight ){}

	
    //__feature_mapping__ [DirectedOnlyVertices] [80:80]
	public int getWeight() { return 0; }

	

    //__feature_mapping__ [DirectedOnlyVertices] [82:85]
	public Vertex getOtherVertex( Vertex vertex )
    {
        return this;
    }

	



    //__feature_mapping__ [DirectedOnlyVertices] [89:91]
	public void adjustAdorns( EdgeIfc the_edge )
    {
    }

	
    public int VertexNumber;

	
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
