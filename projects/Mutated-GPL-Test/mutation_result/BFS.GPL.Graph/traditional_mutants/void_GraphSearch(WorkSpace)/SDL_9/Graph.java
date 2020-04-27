// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;


public class Graph
{

    public  void GraphSearch( WorkSpace w )
    {
        VertexIter vxiter = getVertices();
        if (vxiter.hasNext() == false) {
            return;
        }
        while (vxiter.hasNext()) {
            Vertex v = vxiter.next();
            v.init_vertex( w );
        }
        for (; vxiter.hasNext();) {
            Vertex v = vxiter.next();
            if (!v.visited) {
                w.nextRegionAction( v );
                v.nodeSearch( w );
            }
        }
    }

}
