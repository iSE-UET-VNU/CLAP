// This is a mutant program.
// Author : ysma

package GPL;


public class Graph
{

    public  void run( Vertex s )
    {
        ConnectedComponents();
        original( s );
    }

    public  void ConnectedComponents()
    {
        GraphSearch( new RegionWorkSpace() );
    }

}
