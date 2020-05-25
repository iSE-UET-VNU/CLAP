// This is a mutant program.
// Author : ysma

package GPL; 

import java.util.LinkedList; 


public   class  Edge  extends Neighbor  implements EdgeIfc {
	
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
	private void  adjustAdorns__wrappee__DirectedWithEdges( EdgeIfc the_edge ) {}

	

    //__feature_mapping__ [WeightedWithEdges] [18:22]
	public  void adjustAdorns( EdgeIfc the_edge )
    {
        setWeight( the_edge.getWeight() );
        adjustAdorns__wrappee__DirectedWithEdges( the_edge );
    }

	

    //__feature_mapping__ [WeightedWithEdges] [24:27]
	public  void setWeight( int weight )
    {
        this.weight = -weight;
    }

	

    //__feature_mapping__ [WeightedWithEdges] [29:32]
	public  int getWeight()
    {
        return this.weight;
    }

	

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
	private void  display__wrappee__DirectedWithEdges() {
        System.out.println( " start=" + start.getName() + " end=" + end.getName() );
    }

	

    //__feature_mapping__ [WeightedWithEdges] [34:38]
	public  void display()
    {
        System.out.print( " Weight=" + weight );
        display__wrappee__DirectedWithEdges();
    }

	

    private int weight;

	

    //__feature_mapping__ [WeightedWithEdges] [12:16]
	public  void EdgeConstructor( Vertex the_start, Vertex the_end, int the_weight )
    {
        EdgeConstructor( the_start, the_end );
        weight = the_weight;
    }


}
