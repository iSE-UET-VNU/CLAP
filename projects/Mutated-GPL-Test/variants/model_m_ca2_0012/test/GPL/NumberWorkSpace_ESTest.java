/*
 * This file was automatically generated by EvoSuite
 * Sat Apr 04 04:03:44 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import GPL.NumberWorkSpace;
import GPL.Vertex;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class NumberWorkSpace_ESTest extends NumberWorkSpace_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      NumberWorkSpace numberWorkSpace0 = new NumberWorkSpace();
      // Undeclared exception!
      try { 
        numberWorkSpace0.preVisitAction((Vertex) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.NumberWorkSpace", e);
      }
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      NumberWorkSpace numberWorkSpace0 = new NumberWorkSpace();
      Vertex vertex0 = new Vertex();
      numberWorkSpace0.preVisitAction(vertex0);
      assertEquals(0, vertex0.VertexNumber);
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      NumberWorkSpace numberWorkSpace0 = new NumberWorkSpace();
      Vertex vertex0 = new Vertex();
      vertex0.nodeSearch(numberWorkSpace0);
      numberWorkSpace0.preVisitAction(vertex0);
      assertEquals(0, vertex0.VertexNumber);
  }
}
