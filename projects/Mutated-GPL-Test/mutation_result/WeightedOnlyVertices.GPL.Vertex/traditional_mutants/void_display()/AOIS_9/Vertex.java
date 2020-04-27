// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;


public class Vertex
{

    public LinkedList weightsList;

    public  void VertexConstructor()
    {
        original();
        weightsList = new LinkedList();
    }

    public  void addWeight( int weight )
    {
        weightsList.add( new Integer( weight ) );
    }

    public  void adjustAdorns( Vertex the_vertex, int index )
    {
        int the_weight = ((Integer) the_vertex.weightsList.get( index )).intValue();
        weightsList.add( new Integer( the_weight ) );
        original( the_vertex, index );
    }

    public  void display()
    {
        int s = weightsList.size();
        int i;
        System.out.print( " Weights : " );
        for (i = 0; ++i < s; i++) {
            System.out.print( ((Integer) weightsList.get( i )).intValue() + ", " );
        }
        original();
    }

}
