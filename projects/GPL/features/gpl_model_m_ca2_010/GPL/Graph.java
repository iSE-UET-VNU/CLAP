package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 

//dja: add for performance reasons
import java.util.HashMap; 
import java.util.Map; 

// ***********************************************************************
   
public   class  Graph {
	
    public LinkedList vertices;

	
    public static boolean isDirected = false;

	
      
    //dja: add for performance reasons
    private Map verticesMap;

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Graph( ) 
    {
        vertices = new LinkedList();

	  //dja: add for performance reasons
        verticesMap = new HashMap( );

    }

	
 
    // Fall back method that stops the execution of programs
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
 private void  run__wrappee__UndirectedWithNeighbors( Vertex s )
    {
    }

	
    // Executes Number Vertices
    @featureHouse.FeatureAnnotation(name="Number")
public void run( Vertex s )
     {
       	System.out.println("Number");
        NumberVertices( );
        run__wrappee__UndirectedWithNeighbors( s );
    }

	

    // Adds an edge without weights if Weighted layer is not present
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void addEdge( Vertex start,   Neighbor theNeighbor ) 
    {
        start.addEdge( theNeighbor );
        Vertex end = theNeighbor.neighbor;
        end.addEdge( new  Neighbor( start ) );
    }

	

        
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void addVertex( Vertex v ) 
    {
        vertices.add( v );

	  //dja: add for performance reasons
	  verticesMap.put( v.name, v );
    }

	
   
    // Finds a vertex given its name in the vertices list
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public  Vertex findsVertex( String theName )
    {
        Vertex theVertex;
        
        // if we are dealing with the root
        if ( theName == null )
            return null;

	  //dja: removed for performance reasons
//        for( VertexIter vxiter = getVertices( ); vxiter.hasNext( ); )
//        {
//            theVertex = vxiter.next( );
//            if ( theName.equals( theVertex.getName( ) ) )
//            {
//               return theVertex;
//            }
//        }
//        return null;

	  //dja: add for performance reasons
	  return ( Vertex ) verticesMap.get( theName );

    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
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
                return iter.hasNext(); 
            }
        };
    }

	

    // Finds an Edge given both of its vertices
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public  EdgeIfc findsEdge( Vertex theSource,
                    Vertex theTarget )
       {
	  //dja: performance improvement
        //for( VertexIter vertexiter = getVertices(); vertexiter.hasNext(); )
        // {
	  //	Vertex v1 = vertexiter.next( );
	  //	for( EdgeIter edgeiter = v1.getEdges(); edgeiter.hasNext(); )
        //    {
	  //          EdgeIfc theEdge = edgeiter.next();
	  //		Vertex v2 = theEdge.getOtherVertex( v1 );
        //	      if ( ( v1.getName().equals( theSource.getName() ) &&
        //    	       v2.getName().equals( theTarget.getName() ) ) ||
        //         	     ( v1.getName().equals( theTarget.getName() ) &&
        //          	 v2.getName().equals( theSource.getName() ) ) )
        //        	return theEdge;
        //    }
        //}
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

	


    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void display( ) 
    {
        System.out.println( "******************************************" );
        System.out.println( "Vertices " );
        for ( VertexIter vxiter = getVertices( ); vxiter.hasNext( ) ; )
        {
            vxiter.next( ).display( );
        }

        System.out.println( "******************************************" );
    }

	

    // Adds an edge without weights if Weighted layer is not present
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public EdgeIfc addEdge( Vertex start,  Vertex end )
      {
	  Neighbor e = new Neighbor( end );
        addEdge( start, e );
        return e;
    }

	
    @featureHouse.FeatureAnnotation(name="BFS")
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

	

    @featureHouse.FeatureAnnotation(name="Number")
public void NumberVertices( ) 
    {
        GraphSearch( new NumberWorkSpace( ) );
    }


}
