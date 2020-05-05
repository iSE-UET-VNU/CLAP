package GPL; 

import java.util.LinkedList; 
import java.util.Iterator; 

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

	

    //__feature_mapping__ [BFS] [11:15]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__DirectedWithEdges();
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

	 // of bfsNodeSearch

    //__feature_mapping__ [BFS] [69:76]
	public void display( ) 
    {
        if ( visited )
            System.out.print( "  visited " );
        else
            System.out.println( " !visited " );
        display__wrappee__Number( );
    }

	
    public int VertexNumber;

	
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
