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

	

    //__feature_mapping__ [DFS] [9:13]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__UndirectedWithEdges( );
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

	

     //__feature_mapping__ [Connected] [9:13]
	private void  display__wrappee__Connected( ) 
    {
        System.out.print( " comp# "+ componentNumber + " " );
        display__wrappee__UndirectedWithEdges( );
    }

	 // white ->0, gray ->1, black->2
      
     //__feature_mapping__ [Cycle] [11:14]
	private void  display__wrappee__Cycle() {
        System.out.print( " VertexCycle# " + VertexCycle + " " );
        display__wrappee__Connected();
    }

	 // weight so far from s to it
            
     //__feature_mapping__ [MSTPrim] [14:18]
	private void  display__wrappee__MSTPrim( ) 
    {
        System.out.print( " Pred " + pred + " Key " + key + " " );
        display__wrappee__Cycle( );
    }

	 // of dftNodeSearch

    //__feature_mapping__ [DFS] [47:53]
	public void display( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__MSTPrim( );
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

	
    public int componentNumber;

	
    public int VertexCycle;

	
    public int VertexColor;

	
    public String pred;

	 // the predecessor vertex if any
    public int key;

	
    public boolean visited;

	

    //__feature_mapping__ [DFS] [15:19]
	public void init_vertex( WorkSpace w ) 
    {
        visited = false;
        w.init_vertex( ( Vertex ) this );
    }

	

    //__feature_mapping__ [DFS] [21:45]
	public void nodeSearch( WorkSpace w ) 
    {
        Vertex v;

        // Step 1: Do preVisitAction.
        //            If we've already visited this node return
        w.preVisitAction( ( Vertex ) this );

        if ( visited )
            return;

        // Step 2: else remember that we've visited and
        //         visit all neighbors
        visited = true;

        for ( VertexIter  vxiter = getNeighbors(); vxiter.hasNext(); ) 
        {
            v = vxiter.next( );
            w.checkNeighborAction( ( Vertex ) this, v );
            v.nodeSearch( w );
        }

        // Step 3: do postVisitAction now
        w.postVisitAction( ( Vertex ) this );
    }


}
