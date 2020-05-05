// This is a mutant program.
// Author : ysma

package GPL; 


import java.lang.Integer; 


public  class  CycleWorkSpace  extends WorkSpace {
	

    public boolean AnyCycles;

	

    public int counter;

	

    public boolean isDirected;

	

    public static final int WHITE = 0;

	

    public static final int GRAY = 1;

	

    public static final int BLACK = 2;

	

    //__feature_mapping__ [Cycle] [25:30]
	public CycleWorkSpace( boolean UnDir )
    {
        AnyCycles = false;
        counter = 0;
        isDirected = UnDir;
    }

	

    //__feature_mapping__ [Cycle] [32:36]
	public  void init_vertex( Vertex v )
    {
        v.VertexCycle = Integer.MAX_VALUE;
        v.VertexColor = WHITE;
    }

	

    //__feature_mapping__ [Cycle] [38:44]
	public  void preVisitAction( Vertex v )
    {
        if (v.visited != true) {
            v.VertexCycle = counter;
            v.VertexColor = GRAY;
        }
    }

	

    //__feature_mapping__ [Cycle] [46:50]
	public  void postVisitAction( Vertex v )
    {
        v.VertexColor = BLACK;
        counter--;
    }

	

    //__feature_mapping__ [Cycle] [52:63]
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
