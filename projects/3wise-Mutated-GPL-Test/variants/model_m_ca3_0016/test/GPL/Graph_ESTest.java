/*
 * This file was automatically generated by EvoSuite
 * Tue Apr 14 03:13:54 GMT 2020
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
      graph0.NumberVertices();
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.assignName("m28rk @_@");
      graph0.addVertex(vertex0);
      Vertex vertex1 = graph0.findsVertex("m28rk @_@");
      assertEquals(0, vertex1.getWeight());
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      vertex0.addAdjacent((Vertex) null);
      // Undeclared exception!
      try { 
        graph0.run(vertex0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("GPL.Vertex", e);
      }
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<String> linkedList0 = new LinkedList<String>();
      linkedList0.add("!9-2vM`a=C1}");
      graph0.vertices = linkedList0;
      // Undeclared exception!
      try { 
        graph0.run((Vertex) null);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.String cannot be cast to GPL.Vertex
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
      Vertex vertex0 = new Vertex();
      LinkedList<Integer> linkedList0 = new LinkedList<Integer>();
      vertex0.adjacentVertices = linkedList0;
      linkedList0.add((Integer) vertex0.VertexNumber);
      // Undeclared exception!
      try { 
        graph0.findsEdge(vertex0, vertex0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Integer cannot be cast to GPL.EdgeIfc
         //
         verifyException("GPL.Vertex$2", e);
      }
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.addAdjacent((Vertex) null);
      graph0.addVertex(vertex0);
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
  public void test07()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<Object> linkedList0 = new LinkedList<Object>();
      linkedList0.add((Object) graph0);
      graph0.vertices = linkedList0;
      // Undeclared exception!
      try { 
        graph0.display();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Graph cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph", e);
      }
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
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
  public void test09()  throws Throwable  {
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
  public void test10()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = graph0.findsVertex("V;N");
      // Undeclared exception!
      try { 
        graph0.addAnEdge((Vertex) null, vertex0, 24);
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
  public void test12()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<String> linkedList0 = new LinkedList<String>();
      linkedList0.add("UnBjF;");
      graph0.vertices = linkedList0;
      // Undeclared exception!
      try { 
        graph0.GraphSearch((WorkSpace) null);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.String cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Graph graph0 = new Graph();
      WorkSpace workSpace0 = new WorkSpace();
      graph0.GraphSearch(workSpace0);
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      WorkSpace workSpace0 = new WorkSpace();
      graph0.addVertex(vertex0);
      graph0.addVertex(vertex0);
      graph0.GraphSearch(workSpace0);
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Graph graph0 = new Graph();
      VertexIter vertexIter0 = graph0.getVertices();
      LinkedList<Object> linkedList0 = new LinkedList<Object>();
      graph0.vertices = linkedList0;
      linkedList0.add((Object) vertexIter0);
      // Undeclared exception!
      try { 
        graph0.NumberVertices();
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // GPL.Graph$1 cannot be cast to GPL.Vertex
         //
         verifyException("GPL.Graph$1", e);
      }
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addVertex(vertex0);
      graph0.display();
      assertFalse(Graph.isDirected);
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      graph0.vertices = vertex1.adjacentVertices;
      graph0.addEdge(vertex0, vertex1);
      graph0.addVertex(vertex1);
      graph0.run(vertex0);
      assertTrue(vertex0.visited);
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      vertex0.assignName(" U)G");
      vertex1.assignName(" !visited ");
      vertex0.addAdjacent(vertex1);
      EdgeIfc edgeIfc0 = graph0.findsEdge(vertex0, vertex0);
      assertNull(edgeIfc0);
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      Vertex vertex1 = new Vertex();
      graph0.vertices = vertex1.adjacentVertices;
      graph0.addVertex(vertex1);
      vertex1.assignName("Vertic]v ");
      EdgeIfc edgeIfc0 = graph0.findsEdge(vertex1, vertex0);
      assertNull(edgeIfc0);
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      vertex0.name = ":n+(Z8i";
      graph0.addEdge(vertex0, vertex0);
      Vertex vertex1 = (Vertex)graph0.findsEdge(vertex0, vertex0);
      assertEquals(0, vertex1.VertexNumber);
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addEdge(vertex0, vertex0);
      // Undeclared exception!
      try { 
        graph0.findsEdge(vertex0, vertex0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = graph0.findsVertex((String) null);
      assertNull(vertex0);
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      Graph graph0 = new Graph();
      Vertex vertex0 = new Vertex();
      graph0.addAnEdge(vertex0, vertex0, 0);
      assertNull(vertex0.getName());
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      Graph graph0 = new Graph();
      LinkedList<String> linkedList0 = new LinkedList<String>();
      graph0.vertices = linkedList0;
      linkedList0.add((String) null);
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
}
