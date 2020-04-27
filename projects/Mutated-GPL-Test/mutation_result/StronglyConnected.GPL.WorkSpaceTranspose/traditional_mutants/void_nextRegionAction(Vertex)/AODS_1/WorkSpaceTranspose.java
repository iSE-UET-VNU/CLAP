// This is a mutant program.
// Author : ysma

package GPL;


import java.util.LinkedList;
import java.util.Collections;
import java.util.Comparator;


public class WorkSpaceTranspose extends WorkSpace
{

    int SCCCounter;

    public WorkSpaceTranspose()
    {
        SCCCounter = 0;
    }

    public  void preVisitAction( Vertex v )
    {
        if (v.visited != true) {
            v.strongComponentNumber = SCCCounter;
        }
        ;
    }

    public  void nextRegionAction( Vertex v )
    {
        SCCCounter;
    }

}
