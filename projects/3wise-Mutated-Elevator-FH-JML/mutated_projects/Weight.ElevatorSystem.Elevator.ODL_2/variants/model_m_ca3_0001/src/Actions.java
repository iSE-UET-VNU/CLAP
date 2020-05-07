import ElevatorSystem.Elevator; 
import ElevatorSystem.Environment; 
import ElevatorSystem.Person; 

public  class  Actions {
	

	Environment env;

	

	Elevator e;

	

	//__feature_mapping__ [Base] [11:18]
	public Actions(Environment env, Elevator e) {
		super();
		if (env.getFloors().length < 5)
			throw new IllegalArgumentException(
					"These Actions assume at least 5 Floors!");
		this.env = env;
		this.e = e;
	}

	

	// floor to person relation:
	/*
	 * floor 4: bob floor 3: alice floor 2: angelina floor 1: chuck, bigMac
	 * floor 0: monica
	 */
	//__feature_mapping__ [Base] [25:27]
	public Person bobCall() {
		return new Person("bob", 40, 4, 0, env);
	}

	

	//__feature_mapping__ [Base] [29:31]
	public Person aliceCall() {
		return new Person("alice", 40, 3, 0, env);
	}

	

	//__feature_mapping__ [Base] [33:35]
	public Person angelinaCall() {
		return new Person("angelina", 40, 2, 1, env);
	}

	

	//__feature_mapping__ [Base] [37:39]
	public Person chuckCall() {
		return new Person("chuck", 40, 1, 3, env);
	}

	

	//__feature_mapping__ [Base] [41:43]
	public Person monicaCall() {
		return new Person("monica", 30, 0, 1, env);
	}

	

	//__feature_mapping__ [Base] [45:47]
	public Person bigMacCall() {
		return new Person("BigMac", 150, 1, 3, env);
	}

	

	//__feature_mapping__ [Base] [49:52]
	public void pressInLift0() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(0);
	}

	

	//__feature_mapping__ [Base] [54:57]
	public void pressInLift1() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(1);
	}

	

	//__feature_mapping__ [Base] [59:62]
	public void pressInLift2() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(2);
	}

	

	//__feature_mapping__ [Base] [64:67]
	public void pressInLift3() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(3);
	}

	

	//__feature_mapping__ [Base] [69:72]
	public void pressInLift4() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(4);
	}


}
