/*
 * This file was automatically generated by EvoSuite
 * Sat Apr 04 03:43:10 GMT 2020
 */

package GPL;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import GPL.EdgeIfc;
import GPL.Graph;
import GPL.Vertex;
import GPL.VertexIter;
import GPL.WorkSpace;
import java.util.LinkedList;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Graph_ESTest extends Graph_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.name = "";
      graph0.addVertex(vertex0);
      Vertex vertex1 = graph0.findsVertex("");
      assertEquals("", vertex1.getName());
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Graph graph0 = new Graph();
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
  public void test02()  throws Throwable  {
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
  public void test03()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0, (-1708));
      Vertex vertex1 = new Vertex();
      vertex1.adjacentVertices = vertex0.weightsList;
      // Undeclared exception!
      try { 
        graph0.findsEdge(vertex1, vertex0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.EdgeIfc
         //
         verifyException("GPL.Vertex$2", e);
      }
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentVertices;
      graph0.addAnEdge(vertex0, vertex0, Integer.MAX_VALUE);
      vertex0.weightsList = null;
      // Undeclared exception!
      try { 
        graph0.display();
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
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.weightsList = graph0.vertices;
      graph0.addAnEdge(vertex0, vertex0, 0);
      // Undeclared exception!
      try { 
        graph0.display();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Graph graph0 = new Graph();
      // Undeclared exception!
      try { 
        graph0.addVertex((Vertex) null);
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
      // Undeclared exception!
      try { 
        graph0.addEdge(vertex0, (Vertex) null, 2597);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        graph0.addEdge(vertex0, (Vertex) null);
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
      // Undeclared exception!
      try { 
        graph0.addAnEdge(vertex0, (Vertex) null, 0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      vertex1.weightsList = vertex0.adjacentVertices;
      graph0.addEdge(vertex1, vertex1, 0);
      // Undeclared exception!
      try { 
        graph0.Prim(vertex0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.NeighborIfc
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.vertices = null;
      // Undeclared exception!
      try { 
        graph0.NumberVertices();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0, 0);
      Graph graph1 = graph0.Prim(vertex0);
      graph1.vertices = vertex0.weightsList;
      // Undeclared exception!
      try { 
        graph1.NumberVertices();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
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
  public void test14()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Graph graph1 = graph0.Prim(vertex0);
      graph0.addAnEdge(vertex0, vertex0, 1249);
      WorkSpace workSpace0 = new WorkSpace();
      graph1.vertices = vertex0.weightsList;
      // Undeclared exception!
      try { 
        graph1.GraphSearch(workSpace0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.addAdjacent((Vertex) null);
      Vertex vertex1 = new Vertex();
      vertex1.adjacentVertices = graph0.vertices;
      graph0.addEdge(vertex1, vertex0);
      // Undeclared exception!
      try { 
        graph0.ConnectedComponents();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      graph0.vertices = vertex1.weightsList;
      graph0.addAnEdge(vertex1, vertex0, 0);
      // Undeclared exception!
      try { 
        graph0.ConnectedComponents();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      Graph graph0 = new Graph();
      WorkSpace workSpace0 = new WorkSpace();
      graph0.GraphSearch(workSpace0);
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = graph0.findsVertex((String) null);
      assertNull(vertex0);
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.ConnectedComponents();
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.NumberVertices();
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      Graph graph0 = new Graph();
      VertexIter vertexIter0 = graph0.getVertices();
      assertNotNull(vertexIter0);
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      Graph graph0 = new Graph();
      graph0.display();
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      graph0.addVertex(vertex0);
      WorkSpace workSpace0 = new WorkSpace();
      graph0.GraphSearch(workSpace0);
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentVertices;
      graph0.addAnEdge(vertex0, vertex0, Integer.MAX_VALUE);
      graph0.run(vertex0);
      assertTrue(vertex0.visited);
      assertEquals(0, vertex0.key);
  }

  @Test(timeout = 4000)
  public void test25()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0, 0);
      Vertex vertex1 = new Vertex();
      vertex0.name = "dj1!sKe5O";
      EdgeIfc edgeIfc0 = graph0.findsEdge(vertex0, vertex1);
      assertNull(edgeIfc0);
  }

  @Test(timeout = 4000)
  public void test26()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      Vertex vertex2 = vertex1.assignName("djUJsKM$a");
      vertex0.name = "_{/Bk=h4n";
      graph0.addEdge(vertex1, vertex0);
      EdgeIfc edgeIfc0 = graph0.findsEdge(vertex2, vertex2);
      assertNull(edgeIfc0);
  }

  @Test(timeout = 4000)
  public void test27()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0, 0);
      Vertex vertex1 = vertex0.assignName("djUJsKM$a");
      Vertex vertex2 = (Vertex)graph0.findsEdge(vertex1, vertex0);
      assertEquals(0, vertex2.componentNumber);
  }

  @Test(timeout = 4000)
  public void test28()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentVertices;
      graph0.addVertex(vertex0);
      // Undeclared exception!
      try { 
        graph0.findsEdge(vertex0, vertex0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test29()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentVertices;
      Vertex vertex1 = new Vertex();
      graph0.addVertex(vertex1);
      graph0.addAnEdge(vertex0, vertex0, Integer.MAX_VALUE);
      vertex0.name = "n&6YuyB";
      Graph graph1 = graph0.Prim(vertex1);
      graph1.vertices = graph0.vertices;
      // Undeclared exception!
      try { 
        graph1.Prim(vertex0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test30()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentVertices;
      Vertex vertex1 = new Vertex();
      graph0.addVertex(vertex1);
      vertex0.name = "n&6YuyB";
      Vertex vertex2 = new Vertex();
      Graph graph1 = graph0.Prim(vertex2);
      graph1.Prim(vertex0);
      assertEquals(0, vertex2.key);
      assertEquals(0, vertex0.key);
  }

  @Test(timeout = 4000)
  public void test31()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.vertices = vertex0.adjacentVertices;
      Vertex vertex1 = new Vertex();
      graph0.addVertex(vertex1);
      vertex0.name = "n&6YuyB";
      graph0.addEdge(vertex1, vertex0, 0);
      graph0.Prim(vertex0);
      assertEquals(0, vertex0.key);
  }

  @Test(timeout = 4000)
  public void test32()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<Object> linkedList0 = new LinkedList<Object>();
      linkedList0.add((Object) "");
      graph0.vertices = linkedList0;
      Vertex vertex0 = new Vertex();
      // Undeclared exception!
      try { 
        graph0.run(vertex0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.String cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }
}
