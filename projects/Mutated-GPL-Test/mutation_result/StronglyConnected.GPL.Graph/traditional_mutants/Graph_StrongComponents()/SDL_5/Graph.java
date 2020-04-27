// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;


public class Graph
{

    public  void run( Vertex s )
    {
        System.out.println( "StronglyConnected" );
        Graph gaux = StrongComponents();
        gaux.display();
        original( s );
    }

    public  Graph StrongComponents()
    {
        FinishTimeWorkSpace FTWS = new FinishTimeWorkSpace();
        GraphSearch( FTWS );
        Graph gaux = ComputeTranspose( (Graph) this );
        WorkSpaceTranspose WST = new WorkSpaceTranspose();
        gaux.GraphSearch( WST );
        return gaux;
    }

}
