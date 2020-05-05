package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 

import java.lang.Integer; 
import java.util.Collections; 
import java.util.Comparator; 

// *************************************************************************

public   class  Vertex {
	
    public LinkedList neighbors;

	
    public String name;

	

    //__feature_mapping__ [UndirectedWithEdges] [13:16]
	public Vertex( ) 
    {
        VertexConstructor( );
    }

	

     //__feature_mapping__ [UndirectedWithEdges] [18:22]
	private void  VertexConstructor__wrappee__UndirectedWithEdges( ) 
    {
        name      = null;
        neighbors = new LinkedList( );
    }

	

    //__feature_mapping__ [BFS] [11:15]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__UndirectedWithEdges();
        visited = false;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [24:28]
	public  Vertex assignName( String name ) 
    {
        this.name = name;
        return ( Vertex ) this;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [30:33]
	public String getName( )
    {
        return this.name;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [35:38]
	public LinkedList getNeighborsObj( )
    {
 	  return neighbors;
    }

	


    //__feature_mapping__ [UndirectedWithEdges] [41:55]
	public VertexIter getNeighbors( )
    {
        return new VertexIter( )
        {
            private Iterator iter = neighbors.iterator( );
            public Vertex next( ) 
            { 
              return ( ( Neighbor )iter.next( ) ).end; 
            }
            public boolean hasNext( ) 
            { 
              return iter.hasNext( ); 
            }
        };
    }

	

     //__feature_mapping__ [UndirectedWithEdges] [57:67]
	private void  display__wrappee__UndirectedWithEdges( ) 
    {
        System.out.print( " Node " + name + " connected to: " );

        for ( VertexIter vxiter = getNeighbors( ); vxiter.hasNext( ); )
        {
            System.out.print( vxiter.next().getName() + ", " );
        }

        System.out.println( );
    }

	

     //__feature_mapping__ [Number] [9:13]
	private void  display__wrappee__Number( ) 
    {
        System.out.print( " # "+ VertexNumber + " " );
        display__wrappee__UndirectedWithEdges( );
    }

	

     //__feature_mapping__ [MSTKruskal] [16:22]
	private void  display__wrappee__MSTKruskal() {
        if ( representative == null )
            System.out.print( "Rep null " );
        else
            System.out.print( " Rep " + representative.getName() + " " );
        display__wrappee__Number();
    }

	 // of bfsNodeSearch

    //__feature_mapping__ [BFS] [69:76]
	public void display( ) 
    {
        if ( visited )
            System.out.print( "  visited " );
        else
            System.out.println( " !visited " );
        display__wrappee__MSTKruskal( );
    }

	      
//--------------------
// differences
//--------------------

    //__feature_mapping__ [UndirectedWithEdges] [72:75]
	public void addNeighbor( Neighbor n ) 
    {
        neighbors.add( n );
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [77:91]
	public EdgeIter getEdges( )
    {
        return new EdgeIter( )
        {
            private Iterator iter = neighbors.iterator( );
            public EdgeIfc next( ) 
            { 
              return ( ( EdgeIfc ) ( ( Neighbor )iter.next( ) ).edge );
            }
            public boolean hasNext( ) 
            { 
              return iter.hasNext( ); 
            }
        };
    }

	
    public int VertexNumber;

	
    public  Vertex representative;

	
    public LinkedList members;

	
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
