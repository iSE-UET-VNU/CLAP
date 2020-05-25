package GPL; 

import java.util.LinkedList; 

// *************************************************************************
   
public  class  Neighbor {
	
    public  Vertex end;

	
    public  Edge edge;

	
        
    //__feature_mapping__ [DirectedWithEdges] [11:14]
	public Neighbor() {
        end = null;
        edge = null;
    }

	
        
    //__feature_mapping__ [DirectedWithEdges] [16:19]
	public Neighbor( Vertex v,  Edge e ) {
        end = v;
        edge = e;
    }


}
