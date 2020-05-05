package GPL; 

import java.util.LinkedList; 
import java.util.Collections; 
import java.util.Comparator; 

// of FinishTimeWorkSpace
   
  // DFS Transpose traversal
  // *************************************************************************
   
public  class  WorkSpaceTranspose  extends  WorkSpace {
	
    // Strongly Connected Component Counter
    int SCCCounter;

	
        
    //__feature_mapping__ [StronglyConnected] [16:19]
	public WorkSpaceTranspose()
	{
        SCCCounter = 0;
    }

	
        
    //__feature_mapping__ [StronglyConnected] [21:28]
	public void preVisitAction( Vertex v )
    {
        if ( v.visited!=true ) 
          {
            v.strongComponentNumber = SCCCounter;
        }
        ;
    }

	

    //__feature_mapping__ [StronglyConnected] [30:33]
	public void nextRegionAction( Vertex v ) 
    {
        SCCCounter++;
    }


}
