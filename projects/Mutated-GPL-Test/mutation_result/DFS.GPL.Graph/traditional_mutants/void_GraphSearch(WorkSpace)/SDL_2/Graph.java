// This is a mutant program.
// Author : ysma

package GPL;


public class Graph
{

    public  void GraphSearch( WorkSpace w )
    {
        VertexIter vxiter = getVertices();
        if (vxiter.hasNext() == false) {
            return;
        }
        for (vxiter = getVertices(); vxiter.hasNext();) {
            Vertex v = vxiter.next();
            if (!v.visited) {
                w.nextRegionAction( v );
                v.nodeSearch( w );
            }
        }
    }

}
