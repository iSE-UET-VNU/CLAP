// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;


public class Neighbor implements EdgeIfc, NeighborIfc
{

    public Vertex neighbor;

    public Neighbor()
    {
    }

    public Neighbor( Vertex theNeighbor )
    {
        NeighborConstructor( theNeighbor );
    }

    public  void NeighborConstructor( Vertex theNeighbor )
    {
        neighbor = theNeighbor;
    }

    public  void display()
    {
        System.out.print( neighbor.name + " ," );
    }

    public  Vertex getStart()
    {
        return null;
    }

    public  Vertex getEnd()
    {
        return neighbor;
    }

    public  void setWeight( int weight )
    {
    }

    public  Vertex getOtherVertex( Vertex vertex )
    {
        return neighbor;
    }

    public  void adjustAdorns( EdgeIfc the_edge )
    {
    }

}
