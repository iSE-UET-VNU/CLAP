// This is a mutant program.
// Author : ysma

package GPL;


public class NumberWorkSpace extends WorkSpace
{

    int vertexCounter;

    public NumberWorkSpace()
    {
    }

    public  void preVisitAction( Vertex v )
    {
        if (v.visited != true) {
            v.VertexNumber = vertexCounter++;
        }
    }

}
