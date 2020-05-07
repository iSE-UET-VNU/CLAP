package ElevatorSystem; 

public  class  Person {
	

	private int weight;

	

	private int origin;

	

	private int destination;

	

	private String name;

	

	private boolean destinationReached = false;

	

	//__feature_mapping__ [Base] [15:17]
	public int getWeight() {
		return weight;
	}

	

	//__feature_mapping__ [Base] [19:26]
	public Person(String name, int weight, int origin, int destination, Environment env) {
		super();
		this.name = name;
		this.weight = weight;
		this.origin = origin;
		this.destination = destination;
		env.getFloor(origin).addWaitingPerson(this);
	}

	

	//__feature_mapping__ [Base] [28:30]
	public String getName() {
		return name;
	}

	
	//__feature_mapping__ [Base] [31:33]
	public int getOrigin() {
		return origin;
	}

	

	//__feature_mapping__ [Base] [35:37]
	public int getDestination() {
		return destination;
	}

	

	//__feature_mapping__ [Base] [39:41]
	public void leaveElevator() {
		this.destinationReached = true;
	}

	

	//__feature_mapping__ [Base] [43:45]
	public boolean isDestinationReached() {
		return destinationReached;
	}

	
	
	//__feature_mapping__ [Base] [47:50]
	public void enterElevator(Elevator e) {
		
		e.pressInLiftFloorButton(destination);
	}


}
