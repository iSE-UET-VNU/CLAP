package GPL;

// *****************************************************************
   
public class Graph 
{
    // Executes Connected Components
    public void run( Vertex s )
    {
	     	System.out.println("Connected");
        ConnectedComponents( );
        original( s );
    }

    //day dong 15
    public void ConnectedComponents( ) 
    {
        GraphSearch( new RegionWorkSpace( ) );
    }
}
