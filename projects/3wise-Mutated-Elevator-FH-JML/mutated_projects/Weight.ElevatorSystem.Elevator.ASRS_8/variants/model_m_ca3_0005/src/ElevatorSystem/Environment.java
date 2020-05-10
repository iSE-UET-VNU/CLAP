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

	
	
	 // specification 9
	 /*
	  * The Lift will honor Requests from within the lift as long as it is not empty.
	  * (this is actually a copy of Spec2 with added property that the lift is not empty.
	  */
	/*@ model boolean[] calledAt_Spec9; @*/
	
	//__feature_mapping__ [Empty] [12:17]
	public Environment(int numFloors) {
		floors = new Floor[numFloors];
		for (int i = 0; i < numFloors; i++) {
			floors[i] = new Floor(this, i);
		}
	}

	
	
	//__feature_mapping__ [Empty] [19:21]
	public Floor getFloor(int id) {
		return floors[id];
	}

	
	//__feature_mapping__ [Empty] [22:24]
	public Floor[] getFloors() {
		return floors;
	}

	
	//__feature_mapping__ [Empty] [25:27]
	public boolean isTopFloor(int id) {
		return id == floors.length-1;
	}


}
