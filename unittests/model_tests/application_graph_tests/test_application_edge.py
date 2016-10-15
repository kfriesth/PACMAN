
# pacman imports
from pacman.model.constraints.key_allocator_constraints.\
    key_allocator_contiguous_range_constraint import \
    KeyAllocatorContiguousRangeContraint
from pacman.model.graphs.common.slice import Slice
from pacman.model.graphs.machine.impl.machine_edge import MachineEdge

# unit tests imports
from uinit_test_objects.test_edge import TestEdge
from uinit_test_objects.test_vertex import TestVertex


# general imports
import unittest


class TestApplicationEdgeModel(unittest.TestCase):
    """
    tests which test the application graph object
    """

    def test_create_new_edge(self):
        """
        test that you can create a edge between two vertices
        :return:
        """
        vert1 = TestVertex(10, "New AbstractConstrainedVertex 1", 256)
        vert2 = TestVertex(5, "New AbstractConstrainedVertex 2", 256)
        edge1 = TestEdge(vert1, vert2, "First edge")
        self.assertEqual(edge1.pre_vertex, vert1)
        self.assertEqual(edge1.post_vertex, vert2)

    def test_create_new_edge_without_label(self):
        """
        test initisation of a edge without a label
        :return:
        """
        vert1 = TestVertex(10, "New AbstractConstrainedVertex 1", 256)
        vert2 = TestVertex(5, "New AbstractConstrainedVertex 2", 256)
        edge1 = TestEdge(vert1, vert2)
        self.assertEqual(edge1.pre_vertex, vert1)
        self.assertEqual(edge1.post_vertex, vert2)
        self.assertEqual(edge1.label, None)

    def test_create_new_edge_with_constraint_list(self):
        """
        test initisation of a edge with a constraint
        :return:
        """
        constraints = list()
        constraints.append(KeyAllocatorContiguousRangeContraint())
        vert1 = TestVertex(10, "New AbstractConstrainedVertex 1", 256)
        vert2 = TestVertex(5, "New AbstractConstrainedVertex 2", 256)
        edge1 = TestEdge(vert1, vert2, "edge 1", constraints)
        self.assertEqual(edge1.constraints[0], constraints[0])

    def test_create_new_edge_add_constraint(self):
        """
        test creating a edge and then adding constraints in a list
        :return:
        """
        constraint1 = KeyAllocatorContiguousRangeContraint()
        constraint2 = KeyAllocatorContiguousRangeContraint()
        constr = list()
        constr.append(constraint1)
        constr.append(constraint2)
        vert1 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        vert2 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        edge1 = TestEdge(vert1, vert2, "edge 1")
        edge1.add_constraints(constr)
        for constraint in constr:
            self.assertIn(constraint, edge1.constraints)

    def test_create_new_vertex_add_constraints(self):
        """
        test that  creating a edge and then adding constraints indivusally
        :return:
        """
        constraint1 = KeyAllocatorContiguousRangeContraint()
        constraint2 = KeyAllocatorContiguousRangeContraint()
        constr = list()
        constr.append(constraint1)
        constr.append(constraint2)
        vert1 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        vert2 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        edge1 = TestEdge(vert1, vert2, "edge 1")
        edge1.add_constraint(constraint1)
        edge1.add_constraint(constraint2)

        for constraint in constr:
            self.assertIn(constraint, edge1.constraints)

    def test_create_machine_vertex_from_vertex_with_previous_constraints(self):
        """
        test the create edge command given by the
        TestEdge actually works and generates a edge
        with the same constraints mapped over
        :return:
        """
        constraint1 = KeyAllocatorContiguousRangeContraint()
        vert1 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        v_slice = Slice(0, 9)
        v_from_vert1 = vert1.create_machine_vertex(
            v_slice, vert1.get_resources_used_by_atoms(v_slice, None))
        vert2 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        v_from_vert2 = vert2.create_machine_vertex(
            v_slice, vert2.get_resources_used_by_atoms(v_slice, None))
        edge1 = TestEdge(vert1, vert2, "edge 1")
        edge1.add_constraint(constraint1)

        edge = edge1.create_machine_edge(
            v_from_vert1, v_slice, v_from_vert2, v_slice)
        self.assertIn(constraint1, edge.constraints)

    def test_new_create_machine_vertex_from_vertex_no_constraints(self):
        """
        test the creating of a edge by the TestEdge
        create edge method will actually create a edge of the
        edge type.
        :return:
        """
        vert1 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        v_slice = Slice(0, 9)
        v_from_vert1 = vert1.create_machine_vertex(
            v_slice, vert1.get_resources_used_by_atoms(v_slice, None))
        vert2 = TestVertex(10, "New AbstractConstrainedVertex", 256)
        v_from_vert2 = vert2.create_machine_vertex(
            v_slice, vert2.get_resources_used_by_atoms(v_slice, None))
        edge1 = TestEdge(vert1, vert2, "edge 1")

        edge = edge1.create_machine_edge(
            v_from_vert1, v_slice, v_from_vert2, v_slice)
        self.assertIsInstance(edge, MachineEdge)

    def test_create_new_machine_edge_from_edge(self):
        """
        test that you can use the TestEdge.create-edge
        method and not cause errors
        :return:
        """
        vert1 = TestVertex(10, "New AbstractConstrainedVertex 1", 256)
        v1_slice = Slice(0, 9)
        v_from_vert1 = vert1.create_machine_vertex(
            v1_slice, vert1.get_resources_used_by_atoms(v1_slice, None))
        vert2 = TestVertex(5, "New AbstractConstrainedVertex 2", 256)
        v2_slice = Slice(0, 4)
        v_from_vert2 = vert2.create_machine_vertex(
            v2_slice, vert2.get_resources_used_by_atoms(v2_slice, None))
        edge1 = TestEdge(vert1, vert2, "First edge")
        edge = edge1.create_machine_edge(
            v_from_vert1, v1_slice, v_from_vert2, v2_slice, "First edge")
        self.assertEqual(edge.label, "First edge")
