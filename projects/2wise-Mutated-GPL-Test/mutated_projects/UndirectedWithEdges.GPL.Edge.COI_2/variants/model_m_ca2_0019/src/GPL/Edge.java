package GPL; 

import java.util.LinkedList; 

// *************************************************************************

public  class  Edge  extends Neighbor  implements EdgeIfc {
	
    private  Vertex start;

	

    //__feature_mapping__ [DirectedWithEdges] [10:14]
	public void EdgeConstructor( Vertex the_start,
                      Vertex the_end ) {
        start = the_start;
        end = the_end;
    }

	

    // dja: fix compile error.
//    public void adjustAdorns( Edge the_edge ) {}
    //__feature_mapping__ [DirectedWithEdges] [18:18]
	public void adjustAdorns( EdgeIfc the_edge ) {}

	


    // dja: fix compile error.
    //__feature_mapping__ [DirectedWithEdges] [22:22]
	public void setWeight(int weight){}

	
    //__feature_mapping__ [DirectedWithEdges] [23:23]
	public int getWeight() { return 0; }

	

    //__feature_mapping__ [DirectedWithEdges] [25:33]
	public Vertex getOtherVertex(Vertex vertex)
    {
        if(vertex == start)
            return end;
        else if(vertex == end)
            return start;
        else
            return null;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [35:38]
	public Vertex getStart()
    {
        return start;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [40:43]
	public Vertex getEnd()
    {
        return end;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [45:47]
	public void display() {
        System.out.println( " start=" + start.getName() + " end=" + end.getName() );
    }


}
