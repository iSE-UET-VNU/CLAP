package GPL; 

import java.util.LinkedList; 

// *************************************************************************
  
public  class  Neighbor  implements NeighborIfc {
	
    public  Vertex end;

	
    public  Edge   edge;

	
        
    //__feature_mapping__ [UndirectedWithEdges] [12:16]
	public Neighbor( )
    {
        end = null;
        edge = null;
    }

	
        
    //__feature_mapping__ [UndirectedWithEdges] [18:22]
	public Neighbor( Vertex v,  Edge e )
    {
        end = v;
        edge = e;
    }


}
