// This is a mutant program.
// Author : ysma

package GPL; 


public  class  NumberWorkSpace  extends WorkSpace {
	

    int vertexCounter;

	

    //__feature_mapping__ [Number] [12:15]
	public NumberWorkSpace()
    {
        vertexCounter = 0;
    }

	

    //__feature_mapping__ [Number] [17:22]
	public  void preVisitAction( Vertex v )
    {
        if (v.visited != true) {
            v.VertexNumber = ~vertexCounter++;
        }
    }


}
