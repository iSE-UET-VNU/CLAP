/*
 * This file was automatically generated by EvoSuite
 * Sat Apr 04 03:51:39 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.shaded.org.mockito.Mockito.*;
import static org.evosuite.runtime.EvoAssertions.*;
import GPL.Graph;
import GPL.Neighbor;
import GPL.Vertex;
import GPL.VertexIter;
import GPL.WorkSpace;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.NoSuchElementException;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.evosuite.runtime.ViolatedAssumptionAnswer;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Graph_ESTest extends Graph_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<Object> linkedList0 = new LinkedList<Object>();
      graph0.vertices = linkedList0;
      linkedList0.add((Object) graph0.vertices);
      linkedList0.add((Object) null);
      // Undeclared exception!
      try { 
        graph0.sortVertices((Comparator) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("java.util.ComparableTimSort", e);
      }
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      graph0.addVertex(vertex0);
      // Undeclared exception!
      try { 
        graph0.sortVertices((Comparator) null);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Vertex cannot be cast to java.lang.Comparable
         //
         verifyException("java.util.ComparableTimSort", e);
      }
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.addVertex((Vertex) null);
      // Undeclared exception!
      try { 
        graph0.run((Vertex) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.adjacentNeighbors = graph0.vertices;
      graph0.addEdge(vertex0, vertex0);
      // Undeclared exception!
      try { 
        graph0.run(vertex0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Neighbor cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.vertices = null;
      // Undeclared exception!
      try { 
        graph0.getVertices();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.addVertex((Vertex) null);
      // Undeclared exception!
      try { 
        graph0.findsVertex("`{gbRLB~}zQ51<=");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.addVertex((Vertex) null);
      // Undeclared exception!
      try { 
        graph0.display();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentNeighbors;
      graph0.addVertex(vertex0);
      // Undeclared exception!
      try { 
        graph0.display();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Vertex cannot be cast to GPL.Neighbor
         //
         verifyException("GPL.Vertex$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.vertices = null;
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        graph0.addVertex(vertex0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      Graph.isDirected = false;
      // Undeclared exception!
      try { 
        graph0.addEdge(vertex1, vertex0);
        fail("Expecting exception: NoSuchElementException");
      
      } catch(NoSuchElementException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("java.util.LinkedList", e);
      }
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      Graph graph0 = new Graph();
      // Undeclared exception!
      try { 
        graph0.addEdge((Vertex) null, (Vertex) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      Vertex vertex1 = new Vertex();
      Graph.isDirected = false;
      Vertex vertex2 = graph0.findsVertex("C;[");
      vertex2.adjacentNeighbors = graph0.vertices;
      // Undeclared exception!
      try { 
        graph0.addEdge(vertex1, vertex2);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Vertex cannot be cast to GPL.Neighbor
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      Graph.isDirected = false;
      Neighbor neighbor0 = new Neighbor(vertex1);
      neighbor0.neighbor = vertex0;
      // Undeclared exception!
      try { 
        graph0.addEdge(vertex1, neighbor0);
        fail("Expecting exception: NoSuchElementException");
      
      } catch(NoSuchElementException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("java.util.LinkedList", e);
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = graph0.findsVertex("B:aDtCu7nP}CX");
      Neighbor neighbor0 = new Neighbor(vertex0);
      // Undeclared exception!
      try { 
        graph0.addEdge((Vertex) null, neighbor0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Graph.isDirected = false;
      Vertex vertex1 = new Vertex();
      // Undeclared exception!
      try { 
        graph0.addAnEdge(vertex1, vertex0, 0);
        fail("Expecting exception: NoSuchElementException");
      
      } catch(NoSuchElementException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("java.util.LinkedList", e);
      }
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Graph graph0 = new Graph();
      // Undeclared exception!
      try { 
        graph0.addAnEdge((Vertex) null, (Vertex) null, 0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0);
      graph0.vertices = vertex0.adjacentNeighbors;
      // Undeclared exception!
      try { 
        graph0.NumberVertices();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Neighbor cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      // Undeclared exception!
      try { 
        graph0.GraphSearch((WorkSpace) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      Graph graph0 = new Graph();
      Graph.isDirected = false;
      Vertex vertex0 = new Vertex();
      Neighbor neighbor0 = new Neighbor(vertex0);
      graph0.addEdge(vertex0, neighbor0);
      assertEquals(0, neighbor0.weight);
      assertEquals(0, neighbor0.getWeight());
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      Graph graph0 = new Graph();
      WorkSpace workSpace0 = new WorkSpace();
      graph0.GraphSearch(workSpace0);
      assertTrue(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Neighbor neighbor0 = new Neighbor();
      graph0.addEdge(vertex0, neighbor0);
      assertTrue(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      WorkSpace workSpace0 = new WorkSpace();
      graph0.addVertex(vertex0);
      graph0.GraphSearch(workSpace0);
      assertTrue(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      Graph graph0 = new Graph();
      VertexIter vertexIter0 = graph0.getVertices();
      assertNotNull(vertexIter0);
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      graph0.addVertex(vertex0);
      graph0.NumberVertices();
      assertTrue(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      graph0.run(vertex0);
      assertTrue(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test25()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      graph0.display();
      assertTrue(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test26()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      vertex0.name = vertex0.name;
      vertex0.name = "%tajs ";
      Vertex vertex1 = graph0.findsVertex("%tajs ");
      assertSame(vertex1, vertex0);
  }

  @Test(timeout = 4000)
  public void test27()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = graph0.findsVertex((String) null);
      assertNull(vertex0);
  }

  @Test(timeout = 4000)
  public void test28()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0);
      graph0.vertices = vertex0.adjacentNeighbors;
      WorkSpace workSpace0 = new WorkSpace();
      // Undeclared exception!
      try { 
        graph0.GraphSearch(workSpace0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Neighbor cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test29()  throws Throwable  {
      Graph graph0 = new Graph();
      Comparator<String> comparator0 = (Comparator<String>) mock(Comparator.class, new ViolatedAssumptionAnswer());
      graph0.sortVertices(comparator0);
      assertTrue(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test30()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addAnEdge(vertex0, vertex0, 0);
      assertNull(vertex0.getName());
  }

  @Test(timeout = 4000)
  public void test31()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.addVertex((Vertex) null);
      // Undeclared exception!
      try { 
        graph0.NumberVertices();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test32()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<Integer> linkedList0 = new LinkedList<Integer>();
      graph0.vertices = linkedList0;
      Integer integer0 = new Integer(0);
      linkedList0.add(integer0);
      // Undeclared exception!
      try { 
        graph0.findsVertex("");
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }
}
