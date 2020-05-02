// This is a mutant program.
// Author : ysma

package GPL; 


import java.util.LinkedList; 
import java.util.Iterator; 
import java.util.Collections; 
import java.util.Comparator; 


public   class  Graph {
	
    private LinkedList vertices;

	
    private LinkedList edges;

	
    public static final boolean isDirected = true;

	

    //__feature_mapping__ [DirectedWithEdges] [15:18]
	public Graph() {
        vertices = new LinkedList();
        edges = new LinkedList();
    }

	

    // Fall back method that stops the execution of programs
     //__feature_mapping__ [DirectedWithEdges] [21:21]
	private void  run__wrappee__DirectedWithEdges( Vertex s ) {}

	
    // Executes Number Vertices
    //__feature_mapping__ [Number] [8:13]
	public void run( Vertex s )
     {
       	System.out.println("Number");
        NumberVertices( );
        run__wrappee__DirectedWithEdges( s );
    }

	

    //__feature_mapping__ [DirectedWithEdges] [23:25]
	public void sortEdges(Comparator c) {
        Collections.sort(edges, c);
    }

	

    //__feature_mapping__ [DirectedWithEdges] [27:29]
	public void sortVertices(Comparator c) {
        Collections.sort(vertices, c);
    }

	

    // Adds an edge without weights if Weighted layer is not present
    //__feature_mapping__ [DirectedWithEdges] [32:40]
	public EdgeIfc addEdge(Vertex start,  Vertex end) {
        Edge theEdge = new  Edge();
        theEdge.EdgeConstructor( start, end );
        edges.add( theEdge );
        start.addNeighbor( new  Neighbor( end, theEdge ) );
        //end.addNeighbor( new  Neighbor( start, theEdge ) );

        return theEdge;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [42:44]
	protected void addVertex( Vertex v ) {
        vertices.add( v );
    }

	

    // Finds a vertex given its name in the vertices list
    //__feature_mapping__ [DirectedWithEdges] [47:63]
	public  Vertex findsVertex( String theName )
      {
        Vertex theVertex = null;

        // if we are dealing with the root
        if ( theName==null )
            return null;

        for(VertexIter vxiter = getVertices(); vxiter.hasNext(); )
        {
            theVertex = vxiter.next();
            if ( theName.equals( theVertex.getName() ) )
                return theVertex;
        }

        return theVertex;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [65:71]
	public VertexIter getVertices() {
        return new VertexIter() {
                private Iterator iter = vertices.iterator();
                public Vertex next() { return (Vertex)iter.next(); }
                public boolean hasNext() { return iter.hasNext(); }
            };
    }

	


    //__feature_mapping__ [DirectedWithEdges] [74:80]
	public EdgeIter getEdges() {
        return new EdgeIter() {
                private Iterator iter = edges.iterator();
                public EdgeIfc next() { return (EdgeIfc)iter.next(); }
                public boolean hasNext() { return iter.hasNext(); }
            };
    }

	

    //__feature_mapping__ [DirectedWithEdges] [82:96]
	public void display() {
        int i;

        System.out.println( "******************************************" );
        System.out.println( "Vertices " );
        for ( VertexIter vxiter = getVertices(); vxiter.hasNext() ; )
            vxiter.next().display();

        System.out.println( "******************************************" );
        System.out.println( "Edges " );
        for ( EdgeIter edgeiter = getEdges(); edgeiter.hasNext(); )
            edgeiter.next().display();

        System.out.println( "******************************************" );
    }

	

    //__feature_mapping__ [Number] [15:18]
	public void NumberVertices( ) 
    {
        GraphSearch( new NumberWorkSpace( ) );
    }

	

    //__feature_mapping__ [BFS] [13:30]
	public  void GraphSearch( WorkSpace w )
    {
        VertexIter vxiter = getVertices();
        if (vxiter.hasNext() == false) {
            return;
        }
        while (vxiter.hasNext()) {
            Vertex v = vxiter.next();
            v.init_vertex( w );
        }
        for (vxiter = getVertices(); vxiter.hasNext();) {
            Vertex v = vxiter.next();
            if (v.visited) {
                w.nextRegionAction( v );
                v.nodeSearch( w );
            }
        }
    }


}
