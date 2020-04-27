// This is a mutant program.
// Author : ysma

package GPL;


import java.lang.Integer;


public class CycleWorkSpace extends WorkSpace
{

    public boolean AnyCycles;

    public int counter;

    public boolean isDirected;

    public static final int WHITE = 0;

    public static final int GRAY = 1;

    public static final int BLACK = 2;

    public CycleWorkSpace( boolean UnDir )
    {
        AnyCycles = false;
        counter = 0;
        isDirected = UnDir;
    }

    public  void init_vertex( Vertex v )
    {
        v.VertexCycle = Integer.MAX_VALUE;
        v.VertexColor = WHITE;
    }

    public  void preVisitAction( Vertex v )
    {
        if (v.visited != true) {
            v.VertexCycle = counter++;
            v.VertexColor = GRAY++;
        }
    }

    public  void postVisitAction( Vertex v )
    {
        v.VertexColor = BLACK;
        counter--;
    }

    public  void checkNeighborAction( Vertex vsource, Vertex vtarget )
    {
        if (isDirected) {
            if (vsource.VertexColor == GRAY && vtarget.VertexColor == GRAY) {
                AnyCycles = true;
            }
        } else {
            if (vsource.VertexColor == GRAY && vtarget.VertexColor == GRAY && vsource.VertexCycle != vtarget.VertexCycle + 1) {
                AnyCycles = true;
            }
        }
    }

}
