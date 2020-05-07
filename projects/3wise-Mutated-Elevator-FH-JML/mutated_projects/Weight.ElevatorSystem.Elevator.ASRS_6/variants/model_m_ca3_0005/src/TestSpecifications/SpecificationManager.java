package TestSpecifications; 

public  class  SpecificationManager {
	
	
	//__feature_mapping__ [Base] [5:6]
	public static void setupSpecifications() {
	}

	
	
	/**
	 * -1 : all Specifications of enabled Features
	 * -2 : no Specifications
	 * else : only specification with given number
	 * @param specificationID
	 * @return
	 */
	//__feature_mapping__ [Base] [15:22]
	public static boolean checkSpecification(int id) {
		if (singleSpecification == -2)
			return false;
		else if (singleSpecification == -1)
			return true;
		else 
			return singleSpecification == id;
	}

	

	private static int singleSpecification = -1;

	

	//__feature_mapping__ [Base] [26:28]
	public static void checkOnlySpecification(int scenario) {
		singleSpecification  = scenario;
	}


}
