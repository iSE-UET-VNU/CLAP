package GPL; 

import java.util.LinkedList; 
import java.util.Iterator; 

// ***********************************************************************
  
public   class  Vertex {
	
    public LinkedList adjacentNeighbors;

	
    public String name;

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public Vertex() 
    {
        VertexConstructor();
    }

	
      
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
 private void  VertexConstructor__wrappee__UndirectedWithNeighbors() 
    {
        name      = null;
        adjacentNeighbors = new LinkedList();
    }

	

    @featureHouse.FeatureAnnotation(name="BFS")
public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__UndirectedWithNeighbors();
        visited = false;
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public  Vertex assignName( String name ) 
    {
        this.name = name;
        return ( Vertex ) this;
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public String getName( )
    {
        return this.name;
    }

	
    
    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public LinkedList getNeighborsObj( )
    {
 	  return adjacentNeighbors;
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
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

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
 private void  display__wrappee__UndirectedWithNeighbors( ) 
    {
        System.out.print( "Node " + name + " connected to: " );

        for ( VertexIter vxiter = getNeighbors( ); vxiter.hasNext( ); )
        {
            System.out.print( vxiter.next( ).getName( ) + ", " );
        }

        System.out.println();
    }

	 // of bfsNodeSearch

    @featureHouse.FeatureAnnotation(name="BFS")
 private void  display__wrappee__BFS( ) 
    {
        if ( visited )
            System.out.print( "  visited " );
        else
            System.out.println( " !visited " );
        display__wrappee__UndirectedWithNeighbors( );
    }

	

    @featureHouse.FeatureAnnotation(name="Number")
public void display( ) 
    {
        System.out.print( " # "+ VertexNumber + " " );
        display__wrappee__BFS( );
    }

	
//--------------------
// differences
//--------------------

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void addEdge( Neighbor n ) 
    {
        adjacentNeighbors.add( n );
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
public void adjustAdorns( Neighbor sourceNeighbor )
    {
    }

	

    @featureHouse.FeatureAnnotation(name="UndirectedWithNeighbors")
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

	
    public boolean visited;

	

    @featureHouse.FeatureAnnotation(name="BFS")
public void init_vertex( WorkSpace w ) 
    {
        visited = false;
        w.init_vertex( ( Vertex ) this );
    }

	

    @featureHouse.FeatureAnnotation(name="BFS")
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

	
    public int VertexNumber;


}
