// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;
import java.util.Collections;
import java.util.Comparator;


public class Vertex
{

    public int finishTime;

    public int strongComponentNumber;

    public  void display()
    {
        System.out.print( strongComponentNumber );
        original();
    }

}
