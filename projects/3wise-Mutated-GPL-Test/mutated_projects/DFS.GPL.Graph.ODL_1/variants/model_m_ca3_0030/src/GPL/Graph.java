// This is a mutant program.
// Author : ysma

package GPL; 

//dja - trying to fix logic problems
import java.util.Iterator; 
import java.util.LinkedList; 
//dja: added to fix compile problems when doing the performance improvements
import java.util.Comparator; 
import java.util.Collections; 

import java.lang.Integer; 


public   class  Graph {
	
    public LinkedList vertices;

	
    public static final boolean isDirected = true;

	

    //__feature_mapping__ [DirectedOnlyVertices] [17:19]
	public Graph() {
        vertices = new LinkedList();
    }

	

    //__feature_mapping__ [DirectedOnlyVertices] [21:37]
	public VertexIter getVertices( ) 
    { 
        // dja - trying to fix logic problems
        return new VertexIter( ) 
        {
                private Iterator iter = vertices.iterator( );
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

	
// dja - fix compile code.
//    public EdgeIter getEdges() { return null; }
//    public EdgeIfc addEdge(Vertex start,  Vertex end) { return null; }
//    public  Vertex findsVertex( String theName ) { return null; }

    // Fall back method that stops the execution of programs
     //__feature_mapping__ [DirectedOnlyVertices] [44:44]
	private void  run__wrappee__DirectedOnlyVertices( Vertex s ) {}

	

    // Executes Cycle Checking
    //__feature_mapping__ [Cycle] [12:16]
	public void run( Vertex s )
     {
        System.out.println( "Cycle? " + CycleCheck() );
        run__wrappee__DirectedOnlyVertices( s );
    }

	

    //dja: fix for compile problems during performance improvements
    //__feature_mapping__ [DirectedOnlyVertices] [47:49]
	public void sortVertices(Comparator c) {
        Collections.sort(vertices, c);
    }

	

    // Adds an edge without weights if Weighted layer is not present
    //__feature_mapping__ [DirectedOnlyVertices] [52:55]
	public void addAnEdge( Vertex start,  Vertex end, int weight )
      {
        addEdge( start,end );
    }

	



    //__feature_mapping__ [DirectedOnlyVertices] [59:61]
	public void addVertex( Vertex v ) {
        vertices.add( v );
    }

	

    // Adds and edge by setting end as adjacent to start vertices
    //__feature_mapping__ [DirectedOnlyVertices] [64:67]
	public EdgeIfc addEdge( Vertex start,  Vertex end ) {
        start.addAdjacent( end );
        return( EdgeIfc ) start;
    }

	

    // Finds a vertex given its name in the vertices list
    //__feature_mapping__ [DirectedOnlyVertices] [70:86]
	public  Vertex findsVertex( String theName )
      {
        int i=0;
        Vertex theVertex;

        // if we are dealing with the root
        if ( theName==null )
            return null;

        for( i=0; i<vertices.size(); i++ )
            {
            theVertex = ( Vertex )vertices.get( i );
            if ( theName.equals( theVertex.name ) )
                return theVertex;
        }
        return null;
    }

	

    //__feature_mapping__ [DirectedOnlyVertices] [88:98]
	public void display() {
        int s = vertices.size();
        int i;

        System.out.println( "******************************************" );
        System.out.println( "Vertices " );
        for ( i=0; i<s; i++ )
            ( ( Vertex ) vertices.get( i ) ).display();
        System.out.println( "******************************************" );

    }

	
              
    //__feature_mapping__ [Cycle] [18:22]
	public boolean CycleCheck() {
        CycleWorkSpace c = new CycleWorkSpace( isDirected );
        GraphSearch( c );
        return c.AnyCycles;
    }

	

    //__feature_mapping__ [DFS] [10:27]
	public  void GraphSearch( WorkSpace w )
    {
        VertexIter vxiter = getVertices();
        if (vxiter.hasNext()) {
            return;
        }
        while (vxiter.hasNext()) {
            Vertex v = vxiter.next();
            v.init_vertex( w );
        }
        for (vxiter = getVertices(); vxiter.hasNext();) {
            Vertex v = vxiter.next();
            if (!v.visited) {
                w.nextRegionAction( v );
                v.nodeSearch( w );
            }
        }
    }


}
