package GPL; 

import java.util.LinkedList; 

// *************************************************************************

public  class  Edge  extends Neighbor  implements EdgeIfc {
	
    public Vertex start;

	

    //__feature_mapping__ [UndirectedWithEdges] [11:15]
	public void EdgeConstructor( Vertex the_start, Vertex the_end )
    {
        start = the_start;
        end = the_end;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [17:19]
	public void adjustAdorns( EdgeIfc the_edge ) 
    {
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [21:23]
	public void setWeight(int weight) 
    {
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [25:28]
	public int getWeight( ) 
    { 
        return 0; 
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [30:44]
	public Vertex getOtherVertex( Vertex vertex )
    {
        if( vertex == start )
        { 
            return end;
        }
        else if(vertex == end)
        { 
            return start;
        }
        else
        { 
            return null;
        }
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [46:49]
	public Vertex getStart( )
    {
        return start;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [51:54]
	public Vertex getEnd( )
    {
        return end;
    }

	

    //__feature_mapping__ [UndirectedWithEdges] [56:59]
	public void display( ) 
    {
        System.out.println( " start=" + start.getName() + " end=" + end.getName( ) );
    }


}
