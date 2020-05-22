package GPL; 

import java.util.LinkedList; 
import java.util.Iterator; 

import java.lang.Integer; 

  // *************************************************************************

public   class  Vertex {
	

    // dja: changed neighbors and name to public
    public LinkedList neighbors;

	

    public String name;

	

    //__feature_mapping__ [DirectedWithEdges] [17:17]
	public String getName() { return name; }

	

    //__feature_mapping__ [DirectedWithEdges] [19:21]
	public Vertex() {
        VertexConstructor();
    }

	

     //__feature_mapping__ [DirectedWithEdges] [23:26]
	private void  VertexConstructor__wrappee__DirectedWithEdges() {
        name      = null;
        neighbors = new LinkedList();
    }

	

    //__feature_mapping__ [DFS] [9:13]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__DirectedWithEdges( );
        visited = false;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [28:31]
	public  Vertex assignName( String name ) {
        this.name = name;
        return ( Vertex ) this;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [33:35]
	public void addNeighbor( Neighbor n ) {
        neighbors.add( n );
    }

	

    //__feature_mapping__ [DirectedWithEdges] [37:43]
	public VertexIter getNeighbors() {
        return new VertexIter() {
                private Iterator iter = neighbors.iterator();
                public Vertex next() { return ((Neighbor)iter.next()).end; }
                public boolean hasNext() { return iter.hasNext(); }
            };
    }

	

    //__feature_mapping__ [DirectedWithEdges] [45:58]
	public EdgeIter getEdges()
    {
        return new EdgeIter()
            {
                private Iterator iter = neighbors.iterator();
                /* dja: changed to fix compile error */
//                public EdgeIfc next() { return ((EdgeIfc)  iter.next()).edge; }
                public EdgeIfc next( ) 
                { 
                  return ( ( EdgeIfc ) ( ( Neighbor ) iter.next( ) ).edge ); 
                }
                public boolean hasNext() { return iter.hasNext(); }
            };
    }

	

     //__feature_mapping__ [DirectedWithEdges] [60:70]
	private void  display__wrappee__DirectedWithEdges() {
        System.out.print( " Node " + getName() + " connected to: " );

        for(VertexIter vxiter = getNeighbors(); vxiter.hasNext(); )
         {
            Vertex v = vxiter.next();
            System.out.print( v.getName() + ", " );
        }

        System.out.println();
    }

	

     //__feature_mapping__ [Number] [9:13]
	private void  display__wrappee__Number( ) 
    {
        System.out.print( " # "+ VertexNumber + " " );
        display__wrappee__DirectedWithEdges( );
    }

	 // white ->0, gray ->1, black->2
      
     //__feature_mapping__ [Cycle] [11:14]
	private void  display__wrappee__Cycle() {
        System.out.print( " VertexCycle# " + VertexCycle + " " );
        display__wrappee__Number();
    }

	 // of dftNodeSearch

    //__feature_mapping__ [DFS] [47:53]
	public void display( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__Cycle( );
    }

	
    public int VertexNumber;

	
    public int VertexCycle;

	
    public int VertexColor;

	
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
