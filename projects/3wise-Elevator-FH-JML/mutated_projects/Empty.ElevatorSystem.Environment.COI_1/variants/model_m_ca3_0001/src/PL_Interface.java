import java.util.List;  

public  interface  PL_Interface {
	
	//__feature_mapping__ [Base] [4:4]
	public List<String> getExecutedActions();

	
	//__feature_mapping__ [Base] [5:5]
	public void start(int specification, int variation) throws Throwable;

	
	//__feature_mapping__ [Base] [6:6]
	public void checkOnlySpecification(int specID);

	
	//__feature_mapping__ [Base] [7:7]
	public boolean isAbortedRun();


}
