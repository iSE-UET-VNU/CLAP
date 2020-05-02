/*
 * This file was automatically generated by EvoSuite
 * Tue Apr 14 02:39:21 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import GPL.Edge;
import GPL.EdgeIter;
import GPL.GlobalVarsWrapper;
import GPL.Vertex;
import GPL.VertexIter;
import GPL.WorkSpace;
import java.util.ConcurrentModificationException;
import java.util.LinkedList;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Vertex_ESTest extends Vertex_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      vertex0.neighbors = null;
      LinkedList linkedList0 = edge0.start.getNeighborsObj();
      assertNull(linkedList0);
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      edge0.end.addNeighbor(edge0);
      vertex0.getNeighborsObj();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.name = "ww{YaB/T'DS";
      vertex0.getName();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.name = "";
      vertex0.getName();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      Vertex vertex1 = new Vertex();
      GlobalVarsWrapper.Queue = vertex1.neighbors;
      WorkSpace workSpace0 = new WorkSpace();
      vertex1.addNeighbor(edge0);
      // Undeclared exception!
      try { 
        vertex1.nodeSearch(workSpace0);
        fail("Expecting exception: ConcurrentModificationException");
      
      } catch(ConcurrentModificationException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("java.util.LinkedList$ListItr", e);
      }
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      Vertex vertex1 = edge0.start;
      WorkSpace workSpace0 = new WorkSpace();
      vertex1.representative = edge0.start;
      vertex1.representative.neighbors = null;
      // Undeclared exception!
      try { 
        vertex1.nodeSearch(workSpace0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      LinkedList<Integer> linkedList0 = new LinkedList<Integer>();
      vertex0.neighbors = linkedList0;
      linkedList0.add((Integer) 0);
      WorkSpace workSpace0 = new WorkSpace();
      // Undeclared exception!
      try { 
        vertex0.nodeSearch(workSpace0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.Neighbor
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
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
  public void test08()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      vertex0.neighbors = null;
      // Undeclared exception!
      try { 
        edge0.end.getNeighbors();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.neighbors = null;
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
  public void test10()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      vertex0.neighbors = null;
      // Undeclared exception!
      try { 
        edge0.start.display();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      edge0.end.neighbors = null;
      // Undeclared exception!
      try { 
        edge0.start.addNeighbor(edge0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0, (-3158));
      String string0 = edge0.end.getName();
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      edge0.start.VertexConstructor();
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      VertexIter vertexIter0 = edge0.start.getNeighbors();
      assertNotNull(vertexIter0);
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      Vertex vertex1 = new Vertex();
      WorkSpace workSpace0 = new WorkSpace();
      vertex1.addNeighbor(edge0);
      assertFalse(vertex1.visited);
      
      vertex1.nodeSearch(workSpace0);
      assertTrue(vertex1.visited);
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      WorkSpace workSpace0 = new WorkSpace();
      edge0.end.addNeighbor(edge0);
      edge0.end.nodeSearch(workSpace0);
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      assertFalse(vertex0.visited);
      
      WorkSpace workSpace0 = new WorkSpace();
      vertex0.nodeSearch(workSpace0);
      vertex0.nodeSearch(workSpace0);
      assertTrue(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      WorkSpace workSpace0 = new WorkSpace();
      edge0.start.nodeSearch(workSpace0);
      edge0.start.display();
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      vertex0.representative = edge0.start;
      edge0.start.display();
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = vertex0.assignName((String) null);
      assertFalse(vertex1.visited);
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      edge0.end.addNeighbor(edge0);
      vertex0.display();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      Vertex vertex0 = new Vertex();
      vertex0.getNeighborsObj();
      assertFalse(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      WorkSpace workSpace0 = new WorkSpace();
      edge0.end.init_vertex(workSpace0);
      assertEquals(0, edge0.getWeight());
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      Edge edge0 = new Edge();
      Vertex vertex0 = new Vertex();
      edge0.EdgeConstructor(vertex0, vertex0);
      EdgeIter edgeIter0 = edge0.start.getEdges();
      assertNotNull(edgeIter0);
  }
}
