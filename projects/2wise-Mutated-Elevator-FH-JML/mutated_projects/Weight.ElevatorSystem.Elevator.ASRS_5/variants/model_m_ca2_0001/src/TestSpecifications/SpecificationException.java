package TestSpecifications; 

public  class  SpecificationException  extends RuntimeException {
	
	private static final long serialVersionUID = -6600356723299466152L;

	
	private String specificationName;

	
	
	//__feature_mapping__ [Base] [7:10]
	public SpecificationException(String testCaseName, String message) {
		super(message);
		this.specificationName = testCaseName;
	}

	
	
	//__feature_mapping__ [Base] [12:14]
	public String getSpecificationName() {
		return specificationName;
	}


}
