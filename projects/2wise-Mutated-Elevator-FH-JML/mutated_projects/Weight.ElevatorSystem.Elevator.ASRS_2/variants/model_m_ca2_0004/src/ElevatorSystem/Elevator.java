package ElevatorSystem; 

import java.util.ArrayList; 
import java.util.Arrays; 
import java.util.List; 

public   class  Elevator {
	

	Environment env;

	

	boolean verbose;

	

	int currentFloorID;

	
	public enum  Direction {
		up { 
		//__feature_mapping__ [Base] [16:16]
			@Override public Direction reverse() {return down;}	
		} ,  
		down { 
		//__feature_mapping__ [Base] [19:19]
			@Override public Direction reverse() {return up;}
		}; 
		//__feature_mapping__ [Base] [21:21]
	public abstract Direction reverse();}

	

	Direction currentHeading;

	

	private List<Person> persons = new ArrayList<Person>();

	
	 enum  DoorState {open ,  close}

	;

	

	DoorState doors;

	

	boolean[] floorButtons;

	
	
	//__feature_mapping__ [Base] [33:40]
	public Elevator(Environment env, boolean verbose) {
		this.verbose = verbose;
		this.currentHeading = Direction.up;
		this.currentFloorID = 0;
		this.doors = DoorState.open;
		this.env = env;
		this.floorButtons = new boolean[env.floors.length];
	}

	
	//__feature_mapping__ [Base] [41:48]
	public Elevator(Environment env, boolean verbose, int floor, boolean headingUp) {
		this.verbose = verbose;
		this.currentHeading = (headingUp ? Direction.up : Direction.down);
		this.currentFloorID = floor;
		this.doors = DoorState.open;
		this.env = env;
		this.floorButtons = new boolean[env.floors.length];
	}

	
	
	//__feature_mapping__ [Overloaded] [33:35]
	public boolean isBlocked() {
		return blocked;
	}

	
	
	 //__feature_mapping__ [Base] [54:58]
	private void  enterElevator__wrappee__Base(Person p) {
		persons.add(p);
		p.enterElevator(this);
		if (verbose) System.out.println(p.getName() + " entered the Elevator at Landing " + this.getCurrentFloorID() + ", going to " + p.getDestination());
	}

	

    //__feature_mapping__ [Weight] [29:33]
	public  void enterElevator( Person p )
    {
        enterElevator__wrappee__Base( p );
        weight += p.getWeight();
    }

	
	
	 //__feature_mapping__ [Base] [60:67]
	private boolean  leaveElevator__wrappee__Base(Person p) {
		if (persons.contains(p)) {
			persons.remove(p);
			p.leaveElevator();
			if (verbose) System.out.println(p.getName() + " left the Elevator at Landing " + currentFloorID);
			return true;
		} else return false;
	}

	

    //__feature_mapping__ [Weight] [19:27]
	public  boolean leaveElevator( Person p )
    {
        if (leaveElevator__wrappee__Base( p )) {
            weight /= p.getWeight();
            return true;
        } else {
            return false;
        }
    }

	
	
	/**
	 * Activates the button for the given floor in the lift.
	 * @param floorID
	 */
	/*@ 
	  @ ensures env.calledAt_Spec2[floorID];
	  @*/
	//__feature_mapping__ [Base] [76:79]
	public void pressInLiftFloorButton(int floorID) {
		/*@ set env.calledAt_Spec2[floorID] = true; @*/
		floorButtons[floorID] = true;
	}

	
	//__feature_mapping__ [Base] [80:82]
	private void resetFloorButton(int floorID) {
		floorButtons[floorID] = false;
	}

	
	//__feature_mapping__ [Base] [83:85]
	public /*@pure@*/  int getCurrentFloorID() {
		return currentFloorID;
	}

	
	
	//__feature_mapping__ [Base] [87:89]
	public /*@pure@*/ boolean areDoorsOpen() {
		return doors == DoorState.open;
	}

	

	 /*Specification 3:
	  * The Lift will not change direction while there are calls in the direction it is traveling.
	  */
	// pre: elevator arrived at the current floor, next actions to be done
	/*@ 
	  @ ensures env.calledAt_Spec1[currentFloorID] == env.calledAt_Spec1[currentFloorID] && areDoorsOpen() ? false : env.calledAt_Spec1[currentFloorID];
	  @ ensures \old(getCurrentDirection()) == Direction.up && getCurrentDirection() == Direction.down ==> (\forall int i; getCurrentFloorID() < i && i < numFloors; !buttonForFloorIsPressed(i));
	  @ ensures \old(getCurrentDirection()) == Direction.down && getCurrentDirection() == Direction.up ==> (\forall int i; 0 <= i && i < getCurrentFloorID(); !buttonForFloorIsPressed(i));
	  @*/
	 //__feature_mapping__ [Base] [100:134]
	private void  timeShift__wrappee__Base() {
		//System.out.println("--");
		
		if (stopRequestedAtCurrentFloor()) {
			//System.out.println("Arriving at " +  currentFloorID + ", Doors opening");
			doors = DoorState.open;
			// iterate over a copy of the original list, avoids concurrent modification exception
			for (Person p: new ArrayList<Person>(persons)) {
				if (p.getDestination() == currentFloorID) {
					leaveElevator(p);					
				}
			}
			env.getFloor(currentFloorID).processWaitingPersons(this);
			resetFloorButton(currentFloorID);
		} else {
			if (doors == DoorState.open)  {
				doors = DoorState.close;
				//System.out.println("Doors Closing");
			}
			if (stopRequestedInDirection(currentHeading, true, true)) {
				//System.out.println("Arriving at " + currentFloorID + ", continuing");
				// continue
				continueInDirection(currentHeading);
			} else if (stopRequestedInDirection(currentHeading.reverse(), true, true)) {
				//System.out.println("Arriving at " + currentFloorID + ", reversing direction because of call in other direction");
				// revert direction
				continueInDirection(currentHeading.reverse());
			} else {
				//idle
				//System.out.println("Arriving at " + currentFloorID + ", idle->continuing");
				continueInDirection(currentHeading);
			}
		}
		/*@ set env.calledAt_Spec1[currentFloorID] = env.calledAt_Spec1[currentFloorID] && areDoorsOpen() ? false : env.calledAt_Spec1[currentFloorID] @*/
	}

	
	
	// specification 14
	/* Original: The Lift will answer requests from the executive Floor.
	 * My Version: While there is a request from the executive Floor the lift will not open its doors somewhere else.
	 */
	/*@ 
	  @ ensures isExecutiveFloorCalling() && areDoorsOpen() ==> isExecutiveFloor(e.getCurrentFloorID());
	  @*/
	 //__feature_mapping__ [ExecutiveFloor] [42:44]
	private void  timeShift__wrappee__ExecutiveFloor() {
		timeShift__wrappee__Base();
	}

	

	// specification 10
	/* Original: The Doors of the lift cannot be closed when the lift is overloaded.
	 * MyVersion: The doors are never closed when the lift is overloaded.
	 */
	 // specification 11
	 /* Elevator must not move while it is overloaded.
	  */
	/*@
	  @ ensures \original;
	  @ ensures weight > maximumWeight ==> areDoorsOpen();
	  @ ensures \old(weight) > \old(maximumWeight) ==> getCurrentFloorID() == \old(getCurrentFloorID());
	  @*/
	//__feature_mapping__ [Overloaded] [23:31]
	public void timeShift() {
		if (areDoorsOpen() && weight > maximumWeight) {
			blocked = true;
			if (verbose) System.out.println("Elevator blocked due to overloading (weight:" + weight + " > maximumWeight:" + maximumWeight + ")");
		} else {
			blocked = false;
			timeShift__wrappee__ExecutiveFloor();
		}
	}

	

	 //__feature_mapping__ [Base] [136:139]
	private boolean  stopRequestedAtCurrentFloor__wrappee__Base() {
		return env.getFloor(currentFloorID).hasCall() 
				|| floorButtons[currentFloorID] == true;
	}

	
	
	// alternative implementation: subclass of "ExecutiveFloor extends Floor"
	 //__feature_mapping__ [ExecutiveFloor] [21:25]
	private boolean  stopRequestedAtCurrentFloor__wrappee__ExecutiveFloor() { //executive
		if (isExecutiveFloorCalling() && !isExecutiveFloor(currentFloorID)) {
			return false;
		} else return stopRequestedAtCurrentFloor__wrappee__Base();
	}

	

	//__feature_mapping__ [TwoThirdsFull] [9:13]
	private boolean stopRequestedAtCurrentFloor() {
		if (weight > maximumWeight*2/3) {
			return floorButtons[currentFloorID] == true;
		} else return stopRequestedAtCurrentFloor__wrappee__ExecutiveFloor();
	}

	
	
	 //__feature_mapping__ [Base] [141:159]
	private void  continueInDirection__wrappee__Base(Direction dir) {
		currentHeading = dir;
		if (currentHeading == Direction.up) {
			if (env.isTopFloor(currentFloorID)) {
				//System.out.println("Reversing at Top Floor");
				currentHeading = currentHeading.reverse();
			}
		} else { 
			if (currentFloorID == 0) {
				//System.out.println("Reversing at Basement Floor");
				currentHeading = currentHeading.reverse();
			}
		}
		if (currentHeading == Direction.up) {
			currentFloorID = currentFloorID + 1;
		} else {
			currentFloorID = currentFloorID - 1;
		}
	}

	
	
	// specification 13
	// Car calls have precedence when the Lift is two thirds full.
	/*@
	  @ ensures \original;
	  @ ensures getCurrentFloorID() != \old(getCurrentFloorID()) &&
	  @   weight > maximumWeight*2/3 ==> 
	  @ 	(\old(getCurrentDirection()) == Direction.up &&
	  @ 	 existInLiftCallsInDirection(Direction.down) && 
	  @ 	 !existInLiftCallsInDirection(Direction.up) ==>
	  @ 	 getCurrentDirection() != Direction.up) &&
	  @ 	(\old(getCurrentDirection()) == Direction.down &&
	  @ 	 existInLiftCallsInDirection(Direction.up) && 
	  @ 	 !existInLiftCallsInDirection(Direction.down) ==>
	  @ 	 getCurrentDirection() != Direction.down);
	  @*/
	//__feature_mapping__ [TwoThirdsFull] [37:39]
	private void continueInDirection(Direction dir) {
		continueInDirection__wrappee__Base(dir);
	}

	

	
	//__feature_mapping__ [Base] [162:167]
	private boolean isAnyLiftButtonPressed() {
		for (int i = 0; i < this.floorButtons.length; i++) {
			if (floorButtons[i]) return true;
		}
		return false;
	}

	
	
	 //__feature_mapping__ [Base] [169:186]
	private boolean  stopRequestedInDirection__wrappee__Base (Direction dir, boolean respectFloorCalls, boolean respectInLiftCalls) {
		Floor[] floors = env.getFloors();
		if (dir == Direction.up) {
			if (env.isTopFloor(currentFloorID)) return false;
			for (int i = currentFloorID+1; i < floors.length; i++) {
				if (respectFloorCalls && floors[i].hasCall()) return true;
				if (respectInLiftCalls && this.floorButtons[i]) return true; 
			}
			return false;
		} else {
			if (currentFloorID == 0) return false;
			for (int i = currentFloorID-1; i >= 0; i--) {
				if (respectFloorCalls && floors[i].hasCall()) return true;
				if (respectInLiftCalls && this.floorButtons[i]) return true;
			}
			return false;
		}
	}

	
	
	 //__feature_mapping__ [ExecutiveFloor] [27:33]
	private boolean  stopRequestedInDirection__wrappee__ExecutiveFloor (Direction dir, boolean respectFloorCalls, boolean respectInLiftCalls) {
		if (isExecutiveFloorCalling()) {
			if (verbose) System.out.println("Giving Priority to Executive Floor");
			return ((this.currentFloorID < executiveFloor)  == (dir == Direction.up));
			
		} else return stopRequestedInDirection__wrappee__Base(dir, respectFloorCalls, respectInLiftCalls);
	}

	
	
	//__feature_mapping__ [TwoThirdsFull] [15:20]
	private boolean stopRequestedInDirection (Direction dir, boolean respectFloorCalls, boolean respectInLiftCalls) {
		if (weight > maximumWeight*2/3 && isAnyLiftButtonPressed()) {
			if (verbose) System.out.println("over 2/3 threshold, ignoring calls from FloorButtons until weight is below 2/3*threshold");
			return stopRequestedInDirection__wrappee__ExecutiveFloor(dir, false, respectInLiftCalls);
		} else return stopRequestedInDirection__wrappee__ExecutiveFloor(dir, respectFloorCalls, respectInLiftCalls);
	}

	
	//__feature_mapping__ [Base] [187:194]
	private boolean anyStopRequested () {
		Floor[] floors = env.getFloors();
		for (int i = 0; i < floors.length; i++) {
			if (floors[i].hasCall()) return true;
			else if (this.floorButtons[i]) return true; 
		}
		return false;		
	}

	

	//__feature_mapping__ [Base] [196:198]
	public /*@pure@*/  boolean buttonForFloorIsPressed(int floorID) {
		return this.floorButtons[floorID];
	}

	

	//__feature_mapping__ [Base] [200:202]
	public /*@pure@*/  Direction getCurrentDirection() {
		return currentHeading;
	}

	
	//__feature_mapping__ [Base] [203:205]
	public Environment getEnv() {
		return env;
	}

	
	//__feature_mapping__ [Base] [206:208]
	public boolean isEmpty() {
		return this.persons.isEmpty();
	}

	
	//__feature_mapping__ [Base] [209:211]
	public boolean isIdle() {
		return !anyStopRequested();
	}

	
	
	//__feature_mapping__ [Base] [213:216]
	@Override
	public String toString() {
		return "Elevator " + (areDoorsOpen() ? "[_]" :  "[] ") + " at " + currentFloorID + " heading " + currentHeading;
	}

	

    int weight;

	

    private static final int maximumWeight = 100;

	

	int executiveFloor = 4;

	
	
	//__feature_mapping__ [ExecutiveFloor] [10:10]
	public /*@pure@*/  boolean isExecutiveFloor(int floorID) {return floorID == executiveFloor; }

	

	//private boolean isExecutiveFloor(Floor floor) {return floor.getFloorID() == executiveFloor; }

	//__feature_mapping__ [ExecutiveFloor] [14:18]
	public /*@pure@*/  boolean isExecutiveFloorCalling() {
		for (Floor f : env.floors) 
			if (f.getFloorID() == executiveFloor && f.hasCall()) return true;
		return false;
	}

	

	//__feature_mapping__ [TwoThirdsFull] [41:50]
	private /*@pure@*/  boolean existInLiftCallsInDirection(Direction d) {
		 if (d == Direction.up) {
			 for (int i = getCurrentFloorID(); i < floorButtons.length; i++)
				 if (buttonForFloorIsPressed(i)) return true;
		 } else if (d == Direction.down) {
			 for (int i = getCurrentFloorID(); i >= 0; i--)
				 if (buttonForFloorIsPressed(i)) return true;
		 }
		 return false;		 
	 }

	

	private boolean blocked = false;


}
