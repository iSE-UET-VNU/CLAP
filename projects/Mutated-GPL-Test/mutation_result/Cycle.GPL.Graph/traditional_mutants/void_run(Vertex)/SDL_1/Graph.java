// This is a mutant program.
// Author : ysma

package GPL;


import java.lang.Integer;


public class Graph
{

    public  void run( Vertex s )
    {
        original( s );
    }

    public  boolean CycleCheck()
    {
        CycleWorkSpace c = new CycleWorkSpace( isDirected );
        GraphSearch( c );
        return c.AnyCycles;
    }

}
