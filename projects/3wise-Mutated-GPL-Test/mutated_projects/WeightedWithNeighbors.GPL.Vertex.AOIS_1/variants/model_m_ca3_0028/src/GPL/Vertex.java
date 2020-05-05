// This is a mutant program.
// Author : ysma

package GPL; 

import java.util.Iterator; 

import java.util.LinkedList; 


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

	

    //__feature_mapping__ [BFS] [11:15]
	public void VertexConstructor( ) 
    {
        VertexConstructor__wrappee__DirectedWithNeighbors();
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

	

     //__feature_mapping__ [Number] [9:13]
	private void  display__wrappee__Number( ) 
    {
        System.out.print( " # "+ VertexNumber + " " );
        display__wrappee__DirectedWithNeighbors( );
    }

	 // of bfsNodeSearch

     //__feature_mapping__ [BFS] [69:76]
	private void  display__wrappee__BFS( ) 
    {
        if ( visited )
            System.out.print( "  visited " );
        else
            System.out.println( " !visited " );
        display__wrappee__Number( );
    }

	

    //__feature_mapping__ [WeightedWithNeighbors] [24:27]
	public  void display()
    {
        display__wrappee__BFS();
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

	

    //__feature_mapping__ [WeightedWithNeighbors] [10:15]
	public  void addWeight( Vertex end, int theWeight )
    {
        Neighbor the_neighbor = (Neighbor) end.adjacentNeighbors.removeLast();
        the_neighbor.weight = ++theWeight;
        end.adjacentNeighbors.add( the_neighbor );
    }


}
