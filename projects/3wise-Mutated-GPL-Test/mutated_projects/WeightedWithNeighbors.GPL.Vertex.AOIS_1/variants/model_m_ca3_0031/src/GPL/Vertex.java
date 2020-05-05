// This is a mutant program.
// Author : ysma

package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 
import java.util.Collections; 
import java.util.Comparator; 

import java.lang.Integer; 


public   class  Vertex {
	
    public LinkedList adjacentNeighbors;

	
    public String name;

	
   
    //__feature_mapping__ [DirectedWithNeighbors] [13:15]
	public Vertex() {
        VertexConstructor();
    }

	
    //__feature_mapping__ [DirectedWithNeighbors] [16:19]
	public String getName( ) 
    { 
        return name; 
    }

	

     //__feature_mapping__ [DirectedWithNeighbors] [21:24]
	private void  VertexConstructor__wrappee__DirectedWithNeighbors() {
        name      = null;
        adjacentNeighbors = new LinkedList();
    }

	

    //__feature_mapping__ [DFS] [9:13]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__DirectedWithNeighbors( );
        visited = false;
    }

	

    //__feature_mapping__ [DirectedWithNeighbors] [26:29]
	public  Vertex assignName( String name ) {
        this.name = name;
        return ( Vertex ) this;
    }

	
   
    //__feature_mapping__ [DirectedWithNeighbors] [31:33]
	public void addEdge( Neighbor n ) {
        adjacentNeighbors.add( n );
    }

	


    //__feature_mapping__ [DirectedWithNeighbors] [36:51]
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

	

     //__feature_mapping__ [DirectedWithNeighbors] [53:54]
	private void  adjustAdorns__wrappee__DirectedWithNeighbors( Neighbor sourceNeighbor )
      {}

	

    //__feature_mapping__ [WeightedWithNeighbors] [17:22]
	public  void adjustAdorns( Neighbor sourceNeighbor )
    {
        Neighbor targetNeighbor = (Neighbor) adjacentNeighbors.getLast();
        targetNeighbor.weight = sourceNeighbor.weight;
        adjustAdorns__wrappee__DirectedWithNeighbors( sourceNeighbor );
    }

	
      
     //__feature_mapping__ [DirectedWithNeighbors] [56:66]
	private void  display__wrappee__DirectedWithNeighbors() 
    {
        System.out.print( "Node " + getName( ) + " connected to: " );

        for(VertexIter vxiter = getNeighbors( ); vxiter.hasNext( ); )
         {
            Vertex v = vxiter.next( );
            System.out.print( v.getName( ) + ", " );
        }
        System.out.println( );
    }

	
      
     //__feature_mapping__ [StronglyConnected] [15:19]
	private void  display__wrappee__StronglyConnected() {
        System.out.print( " FinishTime -> " + finishTime + " SCCNo -> " 
                        + strongComponentNumber );
        display__wrappee__DirectedWithNeighbors();
    }

	 // white ->0, gray ->1, black->2
      
     //__feature_mapping__ [Cycle] [11:14]
	private void  display__wrappee__Cycle() {
        System.out.print( " VertexCycle# " + VertexCycle + " " );
        display__wrappee__StronglyConnected();
    }

	 // of dftNodeSearch

     //__feature_mapping__ [DFS] [47:53]
	private void  display__wrappee__DFS( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__Cycle( );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [24:27]
	public  void display()
    {
        display__wrappee__DFS();
    }

	
    public int finishTime;

	
    public int strongComponentNumber;

	
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

	

    //__feature_mapping__ [WeightedWithNeighbors] [10:15]
	public  void addWeight( Vertex end, int theWeight )
    {
        Neighbor the_neighbor = (Neighbor) end.adjacentNeighbors.removeLast();
        the_neighbor.weight = ++theWeight;
        end.adjacentNeighbors.add( the_neighbor );
    }


}
