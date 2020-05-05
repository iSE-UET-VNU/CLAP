package GPL; 

import java.util.LinkedList; 
import java.util.Collections; 
import java.util.Comparator; 

// ***********************************************************************
   
public  class  FinishTimeWorkSpace  extends  WorkSpace {
	
    int FinishCounter;

	
 
    //__feature_mapping__ [StronglyConnected] [12:14]
	public FinishTimeWorkSpace() {
        FinishCounter = 1;
    }

	

    //__feature_mapping__ [StronglyConnected] [16:20]
	public void preVisitAction( Vertex v )
      {
        if ( v.visited!=true )
            FinishCounter++;
    }

	

    //__feature_mapping__ [StronglyConnected] [22:24]
	public void postVisitAction( Vertex v ) {
        v.finishTime = FinishCounter++;
    }


}
