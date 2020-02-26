package GPL; 

import java.util.LinkedList; 

// *************************************************************************
   
public  class  WorkSpace {
	 // supply template actions
    @featureHouse.FeatureAnnotation(name="BFS")
public void init_vertex( Vertex v ) {}

	
    @featureHouse.FeatureAnnotation(name="BFS")
public void preVisitAction( Vertex v ) {}

	
    @featureHouse.FeatureAnnotation(name="BFS")
public void postVisitAction( Vertex v ) {}

	
    @featureHouse.FeatureAnnotation(name="BFS")
public void nextRegionAction( Vertex v ) {}

	
    @featureHouse.FeatureAnnotation(name="BFS")
public void checkNeighborAction( Vertex vsource, 
     Vertex vtarget ) {}


}
