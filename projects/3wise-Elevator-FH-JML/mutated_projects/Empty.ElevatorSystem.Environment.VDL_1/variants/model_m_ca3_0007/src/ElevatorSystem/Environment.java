// This is a mutant program.
// Author : ysma

package ElevatorSystem; 


public   class  Environment {
	
	
	/* Specification 1:
	 * Pressing a landing Button guarantees that the lift will arrive at that landing and open the doors.
	 */
	/*@ model boolean[] calledAt_Spec1; @*/

	/*Specification 2:
	 * Pressing a button inside the lift guarantees that the lift will arrive at that landing and open the doors.
	 */
	/*@ model boolean[] calledAt_Spec2; @*/
		
	Floor[] floors;

	

    //__feature_mapping__ [Base] [21:28]
	public Environment(int numFloors) {
		/*@ set calledAt_Spec1 = new boolean[numFloors]; @*/
		/*@ set calledAt_Spec2 = new boolean[numFloors]; @*/
		floors = new Floor[numFloors];
		for (int i = 0; i < numFloors; i++) {
			floors[i] = new Floor(this, i);
		}
	
        floors = new Floor[numFloors];
        for (int i = 0; numFloors; i++) {
            floors[i] = new Floor( this, i );
        }
    }

	

    //__feature_mapping__ [Empty] [18:21]
	public  Floor getFloor( int id )
    {
        return floors[id];
    }

	

    //__feature_mapping__ [Empty] [23:26]
	public  Floor[] getFloors()
    {
        return floors;
    }

	

    //__feature_mapping__ [Empty] [28:31]
	public  boolean isTopFloor( int id )
    {
        return id == floors.length - 1;
    }


}
