/*
 * This file was automatically generated by EvoSuite
 * Tue Apr 14 04:29:52 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import GPL.Vertex;
import GPL.WorkSpace;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class WorkSpace_ESTest extends WorkSpace_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      WorkSpace workSpace0 = new WorkSpace();
      Vertex vertex0 = new Vertex();
      workSpace0.checkNeighborAction(vertex0, vertex0);
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      WorkSpace workSpace0 = new WorkSpace();
      Vertex vertex0 = new Vertex();
      workSpace0.init_vertex(vertex0);
      assertEquals(0, vertex0.getWeight());
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      WorkSpace workSpace0 = new WorkSpace();
      Vertex vertex0 = new Vertex();
      workSpace0.preVisitAction(vertex0);
      assertNull(vertex0.getName());
  }

  @Test(timeout = 4000)
  public void test3()  throws Throwable  {
      WorkSpace workSpace0 = new WorkSpace();
      Vertex vertex0 = new Vertex();
      workSpace0.nextRegionAction(vertex0);
      assertEquals(0, vertex0.VertexCycle);
  }

  @Test(timeout = 4000)
  public void test4()  throws Throwable  {
      WorkSpace workSpace0 = new WorkSpace();
      Vertex vertex0 = new Vertex();
      workSpace0.postVisitAction(vertex0);
      assertFalse(vertex0.visited);
  }
}
