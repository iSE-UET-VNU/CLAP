// This is a mutant program.
// Author : ysma

package GPL; 

import java.util.LinkedList; 
import java.util.Iterator; 
import java.util.Collections; 
import java.util.Comparator; 

//dja: add for performance reasons
import java.util.HashMap; 
import java.util.Map; 

import java.lang.Integer; 


public   class  Graph {
	
    private LinkedList vertices;

	
    private LinkedList edges;

	
    public static final boolean isDirected = false;

	

    //dja: add for performance reasons
    private Map verticesMap;

	


    //__feature_mapping__ [UndirectedWithEdges] [26:33]
	public Graph() {
        vertices = new LinkedList();
        edges = new LinkedList();

	  //dja: add for performance reasons
        verticesMap = new HashMap( );

    }

	

    // Fall back method that stops the execution of programs
     //__feature_mapping__ [UndirectedWithEdges] [36:36]
	private void  run__wrappee__UndirectedWithEdges( Vertex s ) {}

	
    // Executes Connected Components
     //__feature_mapping__ [Connected] [8:13]
	private void  run__wrappee__Connected( Vertex s )
    {
	     	System.out.println("Connected");
        ConnectedComponents( );
        run__wrappee__UndirectedWithEdges( s );
    }

	

    // Executes Cycle Checking
    //__feature_mapping__ [Cycle] [12:16]
	public void run( Vertex s )
     {
        System.out.println( "Cycle? " + CycleCheck() );
        run__wrappee__Connected( s );
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [38:40]
	public void sortEdges(Comparator c) {
        Collections.sort(edges, c);
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [42:44]
	public void sortVertices(Comparator c) {
        Collections.sort(vertices, c);
    }

	

    // Adds an edge without weights if Weighted layer is not present
    //__feature_mapping__ [UndirectedWithEdges] [47:55]
	public EdgeIfc addEdge(Vertex start,  Vertex end) {
        Edge theEdge = new  Edge();
        theEdge.EdgeConstructor( start, end );
        edges.add( theEdge );
        start.addNeighbor( new  Neighbor( end, theEdge ) );
        end.addNeighbor( new  Neighbor( start, theEdge ) );

        return theEdge;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [57:63]
	protected void addVertex( Vertex v ) {
        vertices.add( v );

	  //dja: add for performance reasons
	  verticesMap.put( v.name, v );

    }

	

    // Finds a vertex given its name in the vertices list
    //__feature_mapping__ [UndirectedWithEdges] [66:85]
	public  Vertex findsVertex( String theName ) {
        Vertex theVertex;

        // if we are dealing with the root
        if ( theName==null )
            return null;

	  //dja: removed for performance reasons
//        for( VertexIter vxiter = getVertices(); vxiter.hasNext(); )
//        {
//            theVertex = vxiter.next();
//            if ( theName.equals( theVertex.getName() ) )
//                return theVertex;
//        }
//        return null;

	  //dja: add for performance reasons
	  return ( Vertex ) verticesMap.get( theName );

    }

	


    //__feature_mapping__ [UndirectedWithEdges] [88:94]
	public VertexIter getVertices() {
        return new VertexIter() {
                private Iterator iter = vertices.iterator();
                public Vertex next() { return (Vertex)iter.next(); }
                public boolean hasNext() { return iter.hasNext(); }
            };
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [96:102]
	public EdgeIter getEdges() {
        return new EdgeIter() {
                private Iterator iter = edges.iterator();
                public EdgeIfc next() { return (EdgeIfc)iter.next(); }
                public boolean hasNext() { return iter.hasNext(); }
            };
    }

	

    // Finds an Edge given both of its vertices
    //__feature_mapping__ [UndirectedWithEdges] [105:122]
	public  EdgeIfc findsEdge( Vertex theSource,
                    Vertex theTarget )
       {
        EdgeIfc theEdge;

	  // dja: performance improvement
      //  for( EdgeIter edgeiter = getEdges(); edgeiter.hasNext(); )
        for( EdgeIter edgeiter = theSource.getEdges(); edgeiter.hasNext(); )
         {
            theEdge = edgeiter.next();
            if ( ( theEdge.getStart().getName().equals( theSource.getName() ) &&
                  theEdge.getEnd().getName().equals( theTarget.getName() ) ) ||
                 ( theEdge.getStart().getName().equals( theTarget.getName() ) &&
                  theEdge.getEnd().getName().equals( theSource.getName() ) ) )
                return theEdge;
        }
        return null;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [124:136]
	public void display() {
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

	

    //__feature_mapping__ [Connected] [15:18]
	public void ConnectedComponents( ) 
    {
        GraphSearch( new RegionWorkSpace( ) );
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
