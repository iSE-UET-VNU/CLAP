// This is a mutant program.
// Author : ysma

package GPL; 


import java.util.LinkedList; 
import java.util.Collections; 
import java.util.Comparator; 


public  class  FinishTimeWorkSpace  extends WorkSpace {
	

    int FinishCounter;

	

    //__feature_mapping__ [StronglyConnected] [17:20]
	public FinishTimeWorkSpace()
    {
        FinishCounter = 1;
    }

	

    //__feature_mapping__ [StronglyConnected] [22:27]
	public  void preVisitAction( Vertex v )
    {
        if (v.visited != true) {
            FinishCounter--;
        }
    }

	

    //__feature_mapping__ [StronglyConnected] [29:32]
	public  void postVisitAction( Vertex v )
    {
        v.finishTime = FinishCounter++;
    }


}
