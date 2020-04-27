// This is a mutant program.
// Author : ysma

package GPL;


import java.lang.Integer;
import java.util.LinkedList;
import java.util.Collections;
import java.util.Comparator;


public class Vertex
{

    public Vertex representative;

    public LinkedList members;

    public  void display()
    {
        if (representative) {
            System.out.print( "Rep null " );
        } else {
            System.out.print( " Rep " + representative.getName() + " " );
        }
        original();
    }

}
