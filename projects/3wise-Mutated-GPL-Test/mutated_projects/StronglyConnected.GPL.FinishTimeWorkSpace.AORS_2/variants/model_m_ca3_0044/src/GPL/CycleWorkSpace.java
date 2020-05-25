package GPL; 

import java.lang.Integer; 

// *************************************************************************
   
public  class  CycleWorkSpace  extends  WorkSpace {
	

    public boolean AnyCycles;

	
    public int     counter;

	
    public boolean isDirected;

	
      
    public static final int WHITE = 0;

	
    public static final int GRAY  = 1;

	
    public static final int BLACK = 2;

	
            
    //__feature_mapping__ [Cycle] [17:21]
	public CycleWorkSpace( boolean UnDir ) {
        AnyCycles = false;
        counter   = 0;
        isDirected = UnDir;
    }

	

    //__feature_mapping__ [Cycle] [23:27]
	public void init_vertex( Vertex v ) 
      {
        v.VertexCycle = Integer.MAX_VALUE;
        v.VertexColor = WHITE; // initialize to white color
    }

	

    //__feature_mapping__ [Cycle] [29:38]
	public void preVisitAction( Vertex v ) {
        
        // This assigns the values on the way in
        if ( v.visited!=true ) 
        { // if it has not been visited then set the
            // VertexCycle accordingly
            v.VertexCycle = counter++;
            v.VertexColor = GRAY; // we make the vertex gray
        }
    }

	

    //__feature_mapping__ [Cycle] [40:44]
	public void postVisitAction( Vertex v ) 
      {
        v.VertexColor = BLACK; // we are done visiting so make it black
        counter--;
    }

	 // of postVisitAction

    //__feature_mapping__ [Cycle] [46:70]
	public void checkNeighborAction( Vertex vsource, 
                     Vertex vtarget ) 
      {
        // if the graph is directed is enough to check that the source node
        // is gray and the adyacent is gray also to find a cycle
        // if the graph is undirected we need to check that the adyacent is not
        // the father, if it is the father the difference in the VertexCount is
        // only one.                                   
        if ( isDirected )
        {
            if ( ( vsource.VertexColor == GRAY ) && ( vtarget.VertexColor == GRAY ) ) 
              {
                AnyCycles = true;
            }
        }
        else
        { // undirected case
            if ( ( vsource.VertexColor == GRAY ) && ( vtarget.VertexColor == GRAY ) 
                 && vsource.VertexCycle != vtarget.VertexCycle+1 ) 
              {
                AnyCycles = true;
            }
        }
        
    }


}
