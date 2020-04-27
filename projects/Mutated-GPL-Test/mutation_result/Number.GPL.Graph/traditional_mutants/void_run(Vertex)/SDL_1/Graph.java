// This is a mutant program.
// Author : ysma

package GPL;


public class Graph
{

    public  void run( Vertex s )
    {
        NumberVertices();
        original( s );
    }

    public  void NumberVertices()
    {
        GraphSearch( new NumberWorkSpace() );
    }

}
