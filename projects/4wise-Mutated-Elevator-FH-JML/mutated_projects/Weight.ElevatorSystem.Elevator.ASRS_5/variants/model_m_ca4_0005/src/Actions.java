package main; 

import ElevatorSystem.Elevator; 
import ElevatorSystem.Environment; 
import ElevatorSystem.Person; 

public  class  Actions {
	

	Environment env;

	

	Elevator e;

	

	//__feature_mapping__ [Base] [13:20]
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
	//__feature_mapping__ [Base] [27:29]
	public Person bobCall() {
		return new Person("bob", 40, 4, 0, env);
	}

	

	//__feature_mapping__ [Base] [31:33]
	public Person aliceCall() {
		return new Person("alice", 40, 3, 0, env);
	}

	

	//__feature_mapping__ [Base] [35:37]
	public Person angelinaCall() {
		return new Person("angelina", 40, 2, 1, env);
	}

	

	//__feature_mapping__ [Base] [39:41]
	public Person chuckCall() {
		return new Person("chuck", 40, 1, 3, env);
	}

	

	//__feature_mapping__ [Base] [43:45]
	public Person monicaCall() {
		return new Person("monica", 30, 0, 1, env);
	}

	

	//__feature_mapping__ [Base] [47:49]
	public Person bigMacCall() {
		return new Person("BigMac", 150, 1, 3, env);
	}

	

	//__feature_mapping__ [Base] [51:54]
	public void pressInLift0() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(0);
	}

	

	//__feature_mapping__ [Base] [56:59]
	public void pressInLift1() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(1);
	}

	

	//__feature_mapping__ [Base] [61:64]
	public void pressInLift2() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(2);
	}

	

	//__feature_mapping__ [Base] [66:69]
	public void pressInLift3() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(3);
	}

	

	//__feature_mapping__ [Base] [71:74]
	public void pressInLift4() {
		if (!e.isEmpty())
			e.pressInLiftFloorButton(4);
	}


}
