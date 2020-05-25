package GPL; 

// dja - trying to fix compile problems
import java.util.Iterator; 

import java.util.LinkedList; 
import java.util.Collections; 
import java.util.Comparator; 

// of Graph
 
// The weighted layer needs to extend Vertex to provide a new 
// LinkedList to hold the  weigths  of the edges
// ************************************************************
 
public   class  Vertex  implements EdgeIfc, NeighborIfc {
	
    public LinkedList adjacentVertices;

	
    public String name;

	
 
    //__feature_mapping__ [DirectedOnlyVertices] [14:16]
	public Vertex() {
        VertexConstructor();
    }

	
  
     //__feature_mapping__ [DirectedOnlyVertices] [18:21]
	private void  VertexConstructor__wrappee__DirectedOnlyVertices() {
        name      = null;
        adjacentVertices = new LinkedList();
    }

	

     //__feature_mapping__ [DFS] [9:13]
	private void  VertexConstructor__wrappee__DFS( ) 
    {
        VertexConstructor__wrappee__DirectedOnlyVertices( );
        visited = false;
    }

	
 
    //__feature_mapping__ [WeightedOnlyVertices] [14:17]
	public void VertexConstructor() {
        VertexConstructor__wrappee__DFS();
        weightsList = new LinkedList();
    }

	

    //__feature_mapping__ [DirectedOnlyVertices] [23:26]
	public  Vertex assignName( String name ) {
        this.name = name;
        return ( Vertex ) this;
    }

	

    //dja: fix for compile errors during performance improvements
    //__feature_mapping__ [DirectedOnlyVertices] [29:32]
	public String getName( ) 
    { 
        return name; 
    }

	

 
    //__feature_mapping__ [DirectedOnlyVertices] [35:37]
	public void addAdjacent( Vertex n ) {
        adjacentVertices.add( n );
    }

	

     //__feature_mapping__ [DirectedOnlyVertices] [39:40]
	private void  adjustAdorns__wrappee__DirectedOnlyVertices( Vertex the_vertex, int index ) 
      {}

	
    
    //__feature_mapping__ [WeightedOnlyVertices] [24:29]
	public void adjustAdorns( Vertex the_vertex, int index )
    {
        int the_weight = ( ( Integer )the_vertex.weightsList.get( index ) ).intValue();
        weightsList.add( new Integer( the_weight ) );
        adjustAdorns__wrappee__DirectedOnlyVertices( the_vertex, index );
    }

	
      
    // dja - trying to fix compile errors
    //__feature_mapping__ [DirectedOnlyVertices] [43:58]
	public VertexIter getNeighbors( ) 
    {
        return new VertexIter( ) 
        {
            private Iterator iter = adjacentVertices.iterator( );
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

	


     //__feature_mapping__ [DirectedOnlyVertices] [61:70]
	private void  display__wrappee__DirectedOnlyVertices() {
        int s = adjacentVertices.size();
        int i;

        System.out.print( "Vertex " + name + " connected to: " );

        for ( i=0; i<s; i++ )
            System.out.print( ( ( Vertex )adjacentVertices.get( i ) ).name+", " );
        System.out.println();
    }

	

     //__feature_mapping__ [Number] [12:16]
	private  void  display__wrappee__Number()
    {
        System.out.print( " # " + ++VertexNumber + " " );
        display__wrappee__DirectedOnlyVertices();
    }

	
      
     //__feature_mapping__ [StronglyConnected] [15:19]
	private void  display__wrappee__StronglyConnected() {
        System.out.print( " FinishTime -> " + finishTime + " SCCNo -> " 
                        + strongComponentNumber );
        display__wrappee__Number();
    }

	 // of dftNodeSearch

     //__feature_mapping__ [DFS] [47:53]
	private void  display__wrappee__DFS( ) {
        if ( visited )
            System.out.print( "  visited" );
        else
            System.out.println( " !visited " );
        display__wrappee__StronglyConnected( );
    }

	
                          
    //__feature_mapping__ [WeightedOnlyVertices] [31:43]
	public void display()
    {
        int s = weightsList.size();
        int i;

        System.out.print( " Weights : " );

        for ( i=0; i<s; i++ ) {
            System.out.print( ( ( Integer )weightsList.get( i ) ).intValue() + ", " );
        }

        display__wrappee__DFS();
    }

	

//--------------------
// from EdgeIfc
//--------------------

    //__feature_mapping__ [DirectedOnlyVertices] [76:76]
	public Vertex getStart( ) { return null; }

	
    //__feature_mapping__ [DirectedOnlyVertices] [77:77]
	public Vertex getEnd( ) { return null; }

	

    //__feature_mapping__ [DirectedOnlyVertices] [79:79]
	public void setWeight( int weight ){}

	
    //__feature_mapping__ [DirectedOnlyVertices] [80:80]
	public int getWeight() { return 0; }

	

    //__feature_mapping__ [DirectedOnlyVertices] [82:85]
	public Vertex getOtherVertex( Vertex vertex )
    {
        return this;
    }

	



    //__feature_mapping__ [DirectedOnlyVertices] [89:91]
	public void adjustAdorns( EdgeIfc the_edge )
    {
    }

	

    public int VertexNumber;

	
    public int finishTime;

	
    public int strongComponentNumber;

	
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

	
    public LinkedList weightsList;

	
         
    //__feature_mapping__ [WeightedOnlyVertices] [19:22]
	public void addWeight( int weight )
    {
        weightsList.add( new Integer( weight ) );
    }


}
