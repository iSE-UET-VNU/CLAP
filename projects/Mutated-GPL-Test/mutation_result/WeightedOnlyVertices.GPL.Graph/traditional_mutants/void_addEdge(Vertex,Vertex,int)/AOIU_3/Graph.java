// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;


public class Graph
{

    public  void addAnEdge( Vertex start, Vertex end, int weight )
    {
        addEdge( start, end, weight );
    }

    public  void addEdge( Vertex start, Vertex end, int weight )
    {
        addEdge( start, end );
        start.addWeight( weight );
        if (isDirected == false) {
            end.addWeight( -weight );
        }
    }

    public  void display()
    {
        original();
    }

}
