package GPL; 


import java.util.LinkedList; 

// *************************************************************************

public   class  Edge  extends Neighbor  implements EdgeIfc {
	

    private Vertex start;

	

    //__feature_mapping__ [DirectedWithEdges] [15:19]
	public  void EdgeConstructor( Vertex the_start, Vertex the_end )
    {
        start = the_start;
        end = the_end;
    }

	

     //__feature_mapping__ [DirectedWithEdges] [21:23]
	private  void  adjustAdorns__wrappee__DirectedWithEdges( EdgeIfc the_edge )
    {
    }

	

    // Constructor Loophole removed
    // public void EdgeConstructor($TEqn.Vertex the_start,
    //                    $TEqn.Vertex the_end) {
    // Super($TEqn.Vertex, $TEqn.Vertex).EdgeConstructor(the_start,the_end);
    // }

    //__feature_mapping__ [WeightedWithEdges] [20:23]
	public void adjustAdorns( EdgeIfc the_edge ) {
        setWeight(the_edge.getWeight());
        adjustAdorns__wrappee__DirectedWithEdges( the_edge );
    }

	

    //__feature_mapping__ [WeightedWithEdges] [25:28]
	public void setWeight(int weight)
    {
        this.weight = weight;
    }

	

    //__feature_mapping__ [WeightedWithEdges] [30:33]
	public int getWeight()
    {
        return this.weight;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [34:45]
	public  Vertex getOtherVertex( Vertex vertex )
    {
        if (vertex == start) {
            return end;
        } else {
            if (vertex != end) {
                return start;
            } else {
                return null;
            }
        }
    }

	

    //__feature_mapping__ [DirectedWithEdges] [47:50]
	public  Vertex getStart()
    {
        return start;
    }

	

    //__feature_mapping__ [DirectedWithEdges] [52:55]
	public  Vertex getEnd()
    {
        return end;
    }

	

     //__feature_mapping__ [DirectedWithEdges] [57:60]
	private  void  display__wrappee__DirectedWithEdges()
    {
        System.out.println( " start=" + start.getName() + " end=" + end.getName() );
    }

	

    //__feature_mapping__ [WeightedWithEdges] [35:38]
	public void display() {
        System.out.print( " Weight=" + weight );
        display__wrappee__DirectedWithEdges();
    }

	
    private int weight;

	

    //__feature_mapping__ [WeightedWithEdges] [8:12]
	public void EdgeConstructor( Vertex the_start,  Vertex the_end,
                int the_weight ) {
        EdgeConstructor( the_start,the_end );
        weight = the_weight;
    }


}
