/*
 * This file was automatically generated by EvoSuite
 * Sat Apr 04 04:18:26 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import GPL.EdgeIfc;
import GPL.Vertex;
import GPL.VertexIter;
import GPL.WorkSpace;
import java.util.LinkedList;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Vertex_ESTest extends Vertex_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.adjacentVertices = null;
      vertex0.getNeighborsObj();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.addAdjacent(vertex0);
      vertex0.getNeighborsObj();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = vertex0.assignName("HX$5:C d");
      vertex1.getName();
      assertFalse(vertex1.visited);
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.assignName("");
      vertex0.getName();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        vertex0.nodeSearch((WorkSpace) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        vertex0.init_vertex((WorkSpace) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.adjacentVertices = null;
      // Undeclared exception!
      try { 
        vertex0.getNeighbors();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.adjacentVertices = null;
      // Undeclared exception!
      try { 
        vertex0.getEdges();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex$2", e);
      }
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.addAdjacent((Vertex) null);
      // Undeclared exception!
      try { 
        vertex0.display();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      LinkedList<Object> linkedList0 = new LinkedList<Object>();
      vertex0.adjacentVertices = linkedList0;
      linkedList0.add((Object) vertex0.adjacentVertices);
      // Undeclared exception!
      try { 
        vertex0.display();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.util.LinkedList cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        vertex0.adjustAdorns((Vertex) null, 169);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        vertex0.adjustAdorns(vertex0, (-1036));
        fail("Expecting exception: IndexOutOfBoundsException");
      
      } catch(IndexOutOfBoundsException e) {
         //
         // Index: -1036, Size: 0
         //
         verifyException("java.util.LinkedList", e);
      }
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      LinkedList<String> linkedList0 = new LinkedList<String>();
      linkedList0.add("");
      vertex0.weightsList = linkedList0;
      // Undeclared exception!
      try { 
        vertex0.adjustAdorns(vertex0, 0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.String cannot be cast to java.lang.Integer
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      LinkedList<Vertex> linkedList0 = new LinkedList<Vertex>();
      vertex0.weightsList = linkedList0;
      vertex0.weightsList = null;
      // Undeclared exception!
      try { 
        vertex0.addWeight(1);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.adjacentVertices = null;
      // Undeclared exception!
      try { 
        vertex0.addAdjacent(vertex0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      assertFalse(vertex0.visited);
      
      WorkSpace workSpace0 = new WorkSpace();
      vertex0.nodeSearch(workSpace0);
      vertex0.nodeSearch(workSpace0);
      assertTrue(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.VertexConstructor();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.addWeight((-716));
      vertex0.display();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.addAdjacent(vertex0);
      assertFalse(vertex0.visited);
      
      WorkSpace workSpace0 = new WorkSpace();
      vertex0.nodeSearch(workSpace0);
      assertTrue(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      assertFalse(vertex0.visited);
      
      WorkSpace workSpace0 = new WorkSpace();
      vertex0.nodeSearch(workSpace0);
      vertex0.display();
      assertTrue(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.adjustAdorns((EdgeIfc) vertex0);
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.getName();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.setWeight(0);
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.getNeighborsObj();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.addWeight(0);
      vertex0.adjustAdorns(vertex0, 0);
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test25()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.addAdjacent(vertex0);
      vertex0.display();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test26()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.getEnd();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test27()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = vertex0.getOtherVertex(vertex0);
      assertFalse(vertex1.visited);
  }

  @Test(timeout = 4000)
  public void test28()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      VertexIter vertexIter0 = vertex0.getNeighbors();
      WorkSpace workSpace0 = new WorkSpace();
      LinkedList<Object> linkedList0 = new LinkedList<Object>();
      vertex0.adjacentVertices = linkedList0;
      linkedList0.add((Object) vertexIter0);
      // Undeclared exception!
      try { 
        vertex0.nodeSearch(workSpace0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Vertex$1 cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test29()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      int int0 = vertex0.getWeight();
      assertEquals(0, int0);
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test30()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.getStart();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test31()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      WorkSpace workSpace0 = new WorkSpace();
      vertex0.init_vertex(workSpace0);
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test32()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.getEdges();
      assertFalse(vertex0.visited);
  }
}
