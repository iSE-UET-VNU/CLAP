// This is a mutant program.
// Author : ysma

package GPL;


public class RegionWorkSpace extends WorkSpace
{

    int counter;

    public RegionWorkSpace()
    {
        counter = 0;
    }

    public  void init_vertex( Vertex v )
    {
        v.componentNumber =  ;
    }

    public  void postVisitAction( Vertex v )
    {
        v.componentNumber = counter;
    }

    public  void nextRegionAction( Vertex v )
    {
        counter++;
    }

}
