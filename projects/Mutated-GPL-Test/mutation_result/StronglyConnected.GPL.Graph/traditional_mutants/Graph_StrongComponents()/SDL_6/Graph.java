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
        sortVertices( new Comparator(){
            public  int compare( Object o1, Object o2 )
            {
                Vertex v1 = (Vertex) o1;
                Vertex v2 = (Vertex) o2;
                if (v1.finishTime > v2.finishTime) {
                    return -1;
                }
                if (v1.finishTime == v2.finishTime) {
                    return 0;
                }
                return 1;
            }
        } );
        Graph gaux = ComputeTranspose( (Graph) this );
        WorkSpaceTranspose WST = new WorkSpaceTranspose();
        return gaux;
    }

}
