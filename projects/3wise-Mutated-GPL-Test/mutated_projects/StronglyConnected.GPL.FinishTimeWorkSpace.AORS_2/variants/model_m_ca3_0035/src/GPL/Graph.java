package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 

//dja: add for performance reasons
import java.util.HashMap; 
import java.util.Map; 

// ************************************************************
 
public   class  Graph {
	
    public LinkedList vertices;

	
    public static final boolean isDirected = false;

	
    //dja: add for performance reasons
    private Map verticesMap;

	


    //__feature_mapping__ [UndirectedOnlyVertices] [20:26]
	public Graph( )
    {
        vertices = new LinkedList();
	  //dja: add for performance reasons
        verticesMap = new HashMap( );

    }

	

    // Fall back method that stops the execution of programs
     //__feature_mapping__ [UndirectedOnlyVertices] [29:31]
	private void  run__wrappee__UndirectedOnlyVertices( Vertex s )
    {
    }

	
    // Executes Connected Components
    //__feature_mapping__ [Connected] [8:13]
	public void run( Vertex s )
    {
	     	System.out.println("Connected");
        ConnectedComponents( );
        run__wrappee__UndirectedOnlyVertices( s );
    }

	
    // Adds an edge with weights
    //__feature_mapping__ [WeightedOnlyVertices] [9:12]
	public void addAnEdge( Vertex start,  Vertex end, int weight )
   {
        addEdge( start,end, weight );
    }

	

    // Adds and edge by setting start as adjacent to end and
    // viceversa
    //__feature_mapping__ [UndirectedOnlyVertices] [41:46]
	public EdgeIfc addEdge( Vertex start,  Vertex end )
    {
        start.addAdjacent( end );
        end.addAdjacent( start );
        return ( EdgeIfc ) start;
    }

	

     // Adds an edge without weights if Weighted layer is not present
 //   public void addEdge( Vertex start,   NeighborIfc theNeighbor )
   // {
     //   addEdge( Vertex start,  ( Vertex ) theNeighbor )
   // }



    //__feature_mapping__ [UndirectedOnlyVertices] [56:62]
	public void addVertex( Vertex v )
    {
        vertices.add( v );

	  //dja: add for performance reasons
	  verticesMap.put( v.name, v );
    }

	

    // Finds a vertex given its name in the vertices list
    //__feature_mapping__ [UndirectedOnlyVertices] [65:85]
	public  Vertex findsVertex( String theName )
      {
        int i=0;
        Vertex theVertex;

        // if we are dealing with the root
        if ( theName == null )
            return null;

	  //dja: removed for performance reasons
//        for( i=0; i<vertices.size(); i++ )
//        {
//            theVertex = ( Vertex )vertices.get( i );
//            if ( theName.equals( theVertex.name ) )
//                return theVertex;
//        }
//        return null;

	  //dja: add for performance reasons
	  return ( Vertex ) verticesMap.get( theName );
    }

	

    //__feature_mapping__ [UndirectedOnlyVertices] [87:101]
	public VertexIter getVertices( )
    {
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

	

     //__feature_mapping__ [UndirectedOnlyVertices] [103:113]
	private void  display__wrappee__UndirectedOnlyVertices() {
        int s = vertices.size();
        int i;

        System.out.println( "******************************************" );
        System.out.println( "Vertices " );
        for ( i=0; i<s; i++ )
            ( ( Vertex ) vertices.get( i ) ).display();
        System.out.println( "******************************************" );

    }

	
    
    //__feature_mapping__ [WeightedOnlyVertices] [25:28]
	public void display() 
   {
        display__wrappee__UndirectedOnlyVertices();
    }

	
   //__feature_mapping__ [UndirectedOnlyVertices] [114:144]
	public  EdgeIfc findsEdge( Vertex theSource,
                    Vertex theTarget )
       {
        //dja: performance improvement
//        for( VertexIter vertexiter = getVertices(); vertexiter.hasNext(); )
//         {
//        Vertex v1 = vertexiter.next( );
//        for( EdgeIter edgeiter = v1.getEdges(); edgeiter.hasNext(); )
//            {
//                EdgeIfc theEdge = edgeiter.next();
//            Vertex v2 = theEdge.getOtherVertex( v1 );
//              if ( ( v1.getName().equals( theSource.getName() ) &&
//                       v2.getName().equals( theTarget.getName() ) ) ||
//                         ( v1.getName().equals( theTarget.getName() ) &&
//                     v2.getName().equals( theSource.getName() ) ) )
//                    return theEdge;
//            }
//        }
        Vertex v1 = theSource;
        for( EdgeIter edgeiter = v1.getEdges(); edgeiter.hasNext(); )
            {
                EdgeIfc theEdge = edgeiter.next();
            Vertex v2 = theEdge.getOtherVertex( v1 );
              if ( ( v1.getName().equals( theSource.getName() ) &&
                       v2.getName().equals( theTarget.getName() ) ) ||
                         ( v1.getName().equals( theTarget.getName() ) &&
                     v2.getName().equals( theSource.getName() ) ) )
                    return theEdge;
            }
        return null;
    }

	

    //__feature_mapping__ [Connected] [15:18]
	public void ConnectedComponents( ) 
    {
        GraphSearch( new RegionWorkSpace( ) );
    }

	
    //__feature_mapping__ [BFS] [9:35]
	public void GraphSearch( WorkSpace w ) 
    {
        // Step 1: initialize visited member of all nodes
        VertexIter vxiter = getVertices( );
        if ( vxiter.hasNext( ) == false )
        {
            return;
        }

        // Showing the initialization process
        while(vxiter.hasNext( ) ) 
        {
            Vertex v = vxiter.next( );
            v.init_vertex( w );
        }

        // Step 2: traverse neighbors of each node
        for (vxiter = getVertices( ); vxiter.hasNext( ); ) 
        {
            Vertex v = vxiter.next( );
            if ( !v.visited ) 
            {
                w.nextRegionAction( v );
                v.nodeSearch( w );
            }
        } //end for
    }

	
 
    //__feature_mapping__ [WeightedOnlyVertices] [14:23]
	public void addEdge( Vertex start,  Vertex end, int weight )
   {
        addEdge( start,end ); // adds the start and end as adjacent
        start.addWeight( weight ); // the direction layer takes care of that
                
        // if the graph is undirected you have to include 
        // the weight of the edge coming back
        if ( isDirected==false )
            end.addWeight( weight );
    }


}
