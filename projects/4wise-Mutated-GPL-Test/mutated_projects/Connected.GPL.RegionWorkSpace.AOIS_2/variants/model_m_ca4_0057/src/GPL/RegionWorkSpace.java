// This is a mutant program.
// Author : ysma

package GPL; 


public  class  RegionWorkSpace  extends WorkSpace {
	

    int counter;

	

    //__feature_mapping__ [Connected] [12:15]
	public RegionWorkSpace()
    {
        counter = 0;
    }

	

    //__feature_mapping__ [Connected] [17:20]
	public  void init_vertex( Vertex v )
    {
        v.componentNumber = -1;
    }

	

    //__feature_mapping__ [Connected] [22:25]
	public  void postVisitAction( Vertex v )
    {
        v.componentNumber = --counter;
    }

	

    //__feature_mapping__ [Connected] [27:30]
	public  void nextRegionAction( Vertex v )
    {
        counter++;
    }


}
