// This is a mutant program.
// Author : ysma

package GPL;


public class Graph
{

    public  void run( Vertex s )
    {
        System.out.println( "Connected" );
        original( s );
    }

    public  void ConnectedComponents()
    {
        GraphSearch( new RegionWorkSpace() );
    }

}
