// This is a mutant program.
// Author : ysma

package GPL;


public class Graph
{

    public  void addAnEdge( Vertex start, Vertex end, int weight )
    {
        addEdge( start, new Neighbor( end, -weight ) );
    }

    public  void addEdge( Vertex start, Neighbor theNeighbor )
    {
        original( start, theNeighbor );
        if (isDirected == false) {
            Vertex end = theNeighbor.neighbor;
            end.addWeight( end, theNeighbor.weight );
        }
    }

    public  void display()
    {
        original();
    }

}
