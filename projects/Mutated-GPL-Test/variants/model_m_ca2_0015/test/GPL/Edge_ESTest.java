/*
 * This file was automatically generated by EvoSuite
 * Sat Apr 04 04:12:25 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import GPL.Edge;
import GPL.EdgeIfc;
import GPL.Vertex;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Edge_ESTest extends Edge_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      edge0.display();
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Edge edge0 = new Edge();
      edge0.EdgeConstructor((Vertex) null, (Vertex) null, 1);
      int int0 = edge0.getWeight();
      assertEquals(1, int0);
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      Vertex vertex1 = edge0.getStart();
      assertSame(vertex1, vertex0);
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      Vertex vertex1 = edge0.getOtherVertex(vertex0);
      assertEquals(0, vertex1.VertexNumber);
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      Vertex vertex1 = edge0.getEnd();
      assertEquals(0, vertex1.componentNumber);
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      Edge edge0 = new Edge();
      // Undeclared exception!
      try { 
        edge0.adjustAdorns((EdgeIfc) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Edge", e);
      }
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Edge edge0 = new Edge();
      edge0.setWeight(0);
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      Edge edge0 = new Edge();
      int int0 = edge0.getWeight();
      assertEquals(0, int0);
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor((Vertex) null, vertex0, 0);
      Vertex vertex1 = edge0.getOtherVertex(vertex0);
      assertEquals(0, edge0.getWeight());
      assertNull(vertex1);
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = edge0.getOtherVertex(vertex0);
      assertNull(vertex1);
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      Edge edge0 = new Edge();
      // Undeclared exception!
      try { 
        edge0.display();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Edge", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = edge0.getEnd();
      assertNull(vertex0);
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Edge edge0 = new Edge();
      edge0.edge = edge0;
      edge0.edge.EdgeConstructor((Vertex) null, (Vertex) null, (-1025));
      int int0 = edge0.edge.getWeight();
      assertEquals((-1025), int0);
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = edge0.getStart();
      assertNull(vertex0);
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      Edge edge0 = new Edge();
      edge0.adjustAdorns(edge0);
      assertEquals(0, edge0.getWeight());
  }
}
