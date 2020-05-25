package GPL; 

//dja - trying to fix logic problems
import java.util.Iterator; 

import java.util.LinkedList; 
//dja: added to fix compile problems when doing the performance improvements
import java.util.Comparator; 
import java.util.Collections; 

//dja: added for performance improvement
import java.util.HashMap; 
import java.util.Map; 


import java.lang.Integer; 

// **********************************************************************

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

	

    // Executes Strongly Connected Components
     //__feature_mapping__ [StronglyConnected] [11:19]
	private void  run__wrappee__StronglyConnected( Vertex s )
     {
          	System.out.println("StronglyConnected");
        Graph gaux = StrongComponents();
//        Graph.stopProfile();
        gaux.display();
//        Graph.resumeProfile();
        run__wrappee__DirectedOnlyVertices( s );
    }

	

    //__feature_mapping__ [Cycle] [13:17]
	public  void run( Vertex s )
    {
        System.out.println( "Cycle? " );
        run__wrappee__StronglyConnected( s );
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

	

    //__feature_mapping__ [StronglyConnected] [21:55]
	public  Graph StrongComponents() {

        FinishTimeWorkSpace FTWS = new FinishTimeWorkSpace();

        // 1. Computes the finishing times for each vertex
        GraphSearch( FTWS );

        // 2. Order in decreasing  & call DFS Transposal
        sortVertices(
         new Comparator() {
            public int compare( Object o1, Object o2 )
                {
                Vertex v1 = ( Vertex )o1;
                Vertex v2 = ( Vertex )o2;

                if ( v1.finishTime > v2.finishTime )
                    return -1;

                if ( v1.finishTime == v2.finishTime )
                    return 0;
                return 1;
            }
        } );

        // 3. Compute the transpose of G
        // Done at layer transpose
        Graph gaux = ComputeTranspose( ( Graph )this );

        // 4. Traverse the transpose G
        WorkSpaceTranspose WST = new WorkSpaceTranspose();
        gaux.GraphSearch( WST );

        return gaux;

    }

	

    //__feature_mapping__ [Transpose] [13:79]
	public  Graph ComputeTranspose( Graph the_graph )
   {
        int i;
        String theName;

        //dja: added for performance improvement
        Map newVertices = new HashMap( );

        // Creating the new Graph
        Graph newGraph = new  Graph();

        // Creates and adds the vertices with the same name
        for ( VertexIter vxiter = getVertices(); vxiter.hasNext(); )
        {
            theName = vxiter.next().getName();
            //dja: changes for performance improvement
            Vertex v = new  Vertex( ).assignName( theName );
//            newGraph.addVertex( new  Vertex().assignName( theName ) );
            newGraph.addVertex( v );

            //dja: added for performance improvement
            newVertices.put( theName, v );
        }

        Vertex theVertex, newVertex;
        Vertex theNeighbor;
        Vertex newAdjacent;
        EdgeIfc newEdge;

        // adds the transposed edges
        // dja: added line below for performance improvements
        VertexIter newvxiter = newGraph.getVertices( );
        for ( VertexIter vxiter = getVertices(); vxiter.hasNext(); )
        {
            // theVertex is the original source vertex
            // the newAdjacent is the reference in the newGraph to theVertex
            theVertex = vxiter.next();

            // dja: performance improvement fix
            // newAdjacent = newGraph.findsVertex( theVertex.getName() );
            newAdjacent = newvxiter.next( );

            for( VertexIter neighbors = theVertex.getNeighbors(); neighbors.hasNext(); )
            {
                // Gets the neighbor object
                theNeighbor = neighbors.next();

                // the new Vertex is the vertex that was adjacent to theVertex
                // but now in the new graph
                // dja: performance improvement fix
                // newVertex = newGraph.findsVertex( theNeighbor.getName() );
                newVertex = ( Vertex ) newVertices.get( theNeighbor.getName( ) );

                // Creates a new Edge object and adjusts the adornments
                newEdge = newGraph.addEdge( newVertex, newAdjacent );
                //newEdge.adjustAdorns( theNeighbor.edge );

                // Adds the new Neighbor object with the newly formed edge
                // newNeighbor = new $TEqn.Neighbor(newAdjacent, newEdge);
                // (newVertex.neighbors).add(newNeighbor);

            } // all adjacentNeighbors
        } // all the vertices

        return newGraph;

    }

	

    //__feature_mapping__ [Cycle] [19:24]
	public  boolean CycleCheck()
    {
        CycleWorkSpace c = new CycleWorkSpace( isDirected );
        GraphSearch( c );
        return c.AnyCycles;
    }

	
    //__feature_mapping__ [DFS] [7:33]
	public void GraphSearch( WorkSpace w ) 
    {
        // Step 1: initialize visited member of all nodes
        VertexIter vxiter = getVertices( );
        if ( vxiter.hasNext( ) == false )
        {
            return; // if there are no vertices return
        }

        // Initializing the vertices
        while( vxiter.hasNext( ) ) 
        {
            Vertex v = vxiter.next( );
            v.init_vertex( w );
        }

        // Step 2: traverse neighbors of each node
        for( vxiter = getVertices( ); vxiter.hasNext( ); ) 
        {
            Vertex v = vxiter.next( );
            if ( !v.visited ) 
            {
                w.nextRegionAction( v );
                v.nodeSearch( w );
            }
        } 
    }


}
