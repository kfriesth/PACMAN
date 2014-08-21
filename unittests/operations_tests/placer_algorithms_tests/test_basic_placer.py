import unittest
from pacman.model.resources.cpu_cycles_per_tick_resource import \
    CPUCyclesPerTickResource
from pacman.model.resources.dtcm_resource import DTCMResource
from pacman.model.resources.resource_container import ResourceContainer
from pacman.model.resources.sdram_resource import SDRAMResource
from pacman.model.constraints.placer_chip_and_core_constraint import \
    PlacerChipAndCoreConstraint
from pacman.model.constraints.placer_subvertex_same_chip_constraint import \
    PlacerSubvertexSameChipConstraint
from pacman.model.placements.placement import Placement
from pacman.model.placements.placements import Placements
from pacman.exceptions import PacmanPlaceException
from pacman.model.partitioned_graph.partitioned_vertex import PartitionedVertex
from pacman.model.graph_mapper.graph_mapper import GraphMapper
from pacman.model.partitioned_graph.partitioned_graph import PartitionedGraph
from pacman.model.partitionable_graph.partitionable_edge import PartitionableEdge
from pacman.model.partitionable_graph.partitionable_graph import PartitionableGraph
from pacman.model.partitionable_graph.abstract_partitionable_vertex import \
    AbstractPartitionableVertex
from pacman.operations.placer_algorithms.basic_placer import BasicPlacer
from spinn_machine.chip import Chip
from spinn_machine.link import Link
from spinn_machine.machine import Machine
from spinn_machine.processor import Processor
from spinn_machine.router import Router
from spinn_machine.sdram import SDRAM

def get_resources_used_by_atoms(lo_atom, hi_atom, vertex_in_edges):
    vertex = Vertex(1, None)
    cpu_cycles = vertex.get_cpu_usage_for_atoms(lo_atom, hi_atom)
    dtcm_requirement = vertex.get_dtcm_usage_for_atoms(lo_atom, hi_atom)
    sdram_requirement = \
        vertex.get_sdram_usage_for_atoms(lo_atom, hi_atom, vertex_in_edges)
    # noinspection PyTypeChecker
    resources = ResourceContainer(cpu=CPUCyclesPerTickResource(cpu_cycles),
                                  dtcm=DTCMResource(dtcm_requirement),
                                  sdram=SDRAMResource(sdram_requirement))
    return resources


class Vertex(AbstractPartitionableVertex):

    def __init__(self, n_atoms, label):
        AbstractPartitionableVertex.__init__(self, label=label, n_atoms=n_atoms,
                                             max_atoms_per_core=256)
        self._model_based_max_atoms_per_core = 256

    def model_name(self):
        return "test vertex"

    def get_cpu_usage_for_atoms(self, lo_atom, hi_atom):
        return 10 * (hi_atom - lo_atom)

    def get_dtcm_usage_for_atoms(self, lo_atom, hi_atom):
        return 200 * (hi_atom - lo_atom)

    def get_sdram_usage_for_atoms(self, lo_atom, hi_atom, vertex_in_edges):
        return 4000 + (50 * (hi_atom - lo_atom))

class Subvertex(PartitionedVertex):

    def __init__(self, lo_atom, hi_atom, resources_required, label=None,
                 constraints=None):
        PartitionedVertex.__init__(self, lo_atom, hi_atom, resources_required,
                                   label=label, constraints=constraints)
        self._model_based_max_atoms_per_core = 256


class TestBasicPlacer(unittest.TestCase):
    def setUp(self):
        ########################################################################
        #Setting up vertices, edges and graph                                  #
        ########################################################################
        self.vert1 = Vertex(100, "New AbstractConstrainedVertex 1")
        self.vert2 = Vertex(5, "New AbstractConstrainedVertex 2")
        self.vert3 = Vertex(3, "New AbstractConstrainedVertex 3")
        self.edge1 = PartitionableEdge(self.vert1, self.vert2, "First edge")
        self.edge2 = PartitionableEdge(self.vert2, self.vert1, "Second edge")
        self.edge3 = PartitionableEdge(self.vert1, self.vert3, "Third edge")
        self.verts = [self.vert1, self.vert2, self.vert3]
        self.edges = [self.edge1, self.edge2, self.edge3]
        self.graph = PartitionableGraph("Graph", self.verts, self.edges)

        ########################################################################
        #Setting up machine                                                    #
        ########################################################################
        flops = 1000
        (e, ne, n, w, sw, s) = range(6)

        processors = list()
        for i in range(18):
            processors.append(Processor(i, flops))

        links = list()
        links.append(Link(0, 0, 0, 0, 1, s, s))

        _sdram = SDRAM(128*(2**20))

        links = list()

        links.append(Link(0, 0, 0, 1, 1, n, n))
        links.append(Link(0, 1, 1, 1, 0, s, s))
        links.append(Link(1, 1, 2, 0, 0, e, e))
        links.append(Link(1, 0, 3, 0, 1, w, w))
        r = Router(links, False, 100, 1024)

        ip = "192.168.240.253"
        chips = list()
        for x in range(10):
            for y in range(10):
                chips.append(Chip(x, y, processors, r, _sdram, ip))

        self.machine = Machine(chips)
        ########################################################################
        #Setting up subgraph and graph_mapper                                  #
        ########################################################################
        self.subvertices = list()
        self.subvertex1 = Subvertex(
            0, 1, get_resources_used_by_atoms(0, 1, []), "First subvertex")
        self.subvertex2 = Subvertex(
            1, 5, get_resources_used_by_atoms(1, 5, []), "Second subvertex")
        self.subvertex3 = Subvertex(
            5, 10, get_resources_used_by_atoms(5, 10, []), "Third subvertex")
        self.subvertex4 = Subvertex(
            10, 100, get_resources_used_by_atoms(10, 100, []),
            "Fourth subvertex")
        self.subvertices.append(self.subvertex1)
        self.subvertices.append(self.subvertex2)
        self.subvertices.append(self.subvertex3)
        self.subvertices.append(self.subvertex4)
        self.subedges = list()
        self.subgraph = PartitionedGraph("Subgraph", self.subvertices,
                                         self.subedges)
        self.graph_mapper = GraphMapper()
        self.graph_mapper.add_subvertices(self.subvertices)


    def test_new_basic_placer(self):
        self.bp = BasicPlacer(self.machine, self.graph)
        self.assertEqual(self.bp._machine, self.machine)
        self.assertEqual(self.bp._graph, self.graph)

    def test_place_where_subvertices_dont_have_vertex(self):
        self.bp = BasicPlacer(self.machine, self.graph)
        placements = self.bp.place(self.subgraph, self.graph_mapper)
        for placement in placements.placements:
            print placement.subvertex.label, placement.subvertex.n_atoms, \
                'x:', placement.x, 'y:', placement.y, 'p:', placement.p

    def test_place_where_subvertices_have_vertices(self):
        self.bp = BasicPlacer(self.machine, self.graph)
        self.graph_mapper = GraphMapper()
        self.graph_mapper.add_subvertices(self.subvertices, self.vert1)
        placements = self.bp.place(self.subgraph, self.graph_mapper)
        for placement in placements.placements:
            print placement.subvertex.label, placement.subvertex.n_atoms, \
                'x:', placement.x, 'y:', placement.y, 'p:', placement.p

    def test_place_subvertex_too_big_with_vertex(self):
        large_vertex = Vertex(500, "Large vertex 500")
        large_subvertex = large_vertex.create_subvertex(
            0, 499, get_resources_used_by_atoms(0, 499, []))#Subvertex(0, 499, "Large subvertex")
        self.graph.add_vertex(large_vertex)
        self.graph = PartitionableGraph("Graph",[large_vertex])
        self.graph_mapper = GraphMapper()
        self.graph_mapper.add_subvertices([large_subvertex], large_vertex)
        self.bp = BasicPlacer(self.machine, self.graph)
        self.subgraph = PartitionedGraph(subvertices=[large_subvertex])
        with self.assertRaises(PacmanPlaceException):
            placements = self.bp.place(self.subgraph, self.graph_mapper)

    def test_try_to_place(self):
        self.assertEqual(True, False)

    def test_deal_with_constraint_placement_subvertices_dont_have_vertex(self):
        self.bp = BasicPlacer(self.machine, self.graph)
        self.subvertex1.add_constraint(PlacerChipAndCoreConstraint(8, 3, 2))
        self.assertIsInstance(self.subvertex1.constraints[0], PlacerChipAndCoreConstraint)
        self.subvertex2.add_constraint(PlacerChipAndCoreConstraint(3, 5, 7))
        self.subvertex3.add_constraint(PlacerChipAndCoreConstraint(2, 4, 6))
        self.subvertex4.add_constraint(PlacerChipAndCoreConstraint(6, 4, 16))
        self.subvertices = list()
        self.subvertices.append(self.subvertex1)
        self.subvertices.append(self.subvertex2)
        self.subvertices.append(self.subvertex3)
        self.subvertices.append(self.subvertex4)
        self.subedges = list()
        self.subgraph = PartitionedGraph("Subgraph", self.subvertices,
                                         self.subedges)
        self.graph_mapper = GraphMapper()
        self.graph_mapper.add_subvertices(self.subvertices)
        placements = self.bp.place(self.subgraph, self.graph_mapper)
        for placement in placements.placements:
            print placement.subvertex.label, placement.subvertex.n_atoms, \
                'x:', placement.x, 'y:', placement.y, 'p:', placement.p

    def test_deal_with_constraint_placement_subvertices_have_vertices(self):
        self.bp = BasicPlacer(self.machine, self.graph)
        self.subvertex1.add_constraint(PlacerChipAndCoreConstraint(1, 5, 2))
        self.assertIsInstance(self.subvertex1.constraints[0], PlacerChipAndCoreConstraint)
        self.subvertex2.add_constraint(PlacerChipAndCoreConstraint(3, 5, 7))
        self.subvertex3.add_constraint(PlacerChipAndCoreConstraint(2, 4, 6))
        self.subvertex4.add_constraint(PlacerChipAndCoreConstraint(6, 7, 16))
        self.subvertices = list()
        self.subvertices.append(self.subvertex1)
        self.subvertices.append(self.subvertex2)
        self.subvertices.append(self.subvertex3)
        self.subvertices.append(self.subvertex4)
        self.subedges = list()
        self.subgraph = PartitionedGraph("Subgraph", self.subvertices,
                                         self.subedges)
        self.graph_mapper = GraphMapper()
        self.graph_mapper.add_subvertices(self.subvertices, self.vert1)
        placements = self.bp.place(self.subgraph, self.graph_mapper)
        for placement in placements.placements:
            print placement.subvertex.label, placement.subvertex.n_atoms, \
                'x:', placement.x, 'y:', placement.y, 'p:', placement.p

    def test_unsupported_non_placer_constraint(self):
        self.assertEqual(True, False)

    def test_unsupported_placer_constraint(self):
        self.assertEqual(True, False)

    def test_unsupported_placer_constraints(self):
        self.assertEqual(True, False)

    def test_reduce_constraints(self):
        extra_subvertex = PartitionedVertex(
            3, 15, get_resources_used_by_atoms(3, 15, []))
        chip_and_core = PlacerChipAndCoreConstraint(3, 3, 15)
        same_chip_as_vertex = PlacerSubvertexSameChipConstraint(extra_subvertex)
        constrained_subvertex = PartitionedVertex(
            55, 89, get_resources_used_by_atoms(55, 89, []),
            "Constrained vertex", [chip_and_core, same_chip_as_vertex])
        self.subgraph.add_subvertex(constrained_subvertex)
        placement = Placement(constrained_subvertex, 1, 2, 3)
        placement2 = Placement(extra_subvertex, 1, 3, 3)
        placements = Placements([placement, placement2])
        placer = BasicPlacer(self.machine, self.graph)
        constraint = placer._reduce_constraints([chip_and_core,
                                                 same_chip_as_vertex],
                                                constrained_subvertex.label,
                                                placements)

        print constraint.label, 'x:', constraint.x, 'y:', constraint.y, \
            'p:', constraint.p

    def test_reduce_constraints_inverted_order(self):
        extra_subvertex = PartitionedVertex(
            3, 15, get_resources_used_by_atoms(3, 15, []))
        chip_and_core = PlacerChipAndCoreConstraint(3, 3, 15)
        same_chip_as_vertex = PlacerSubvertexSameChipConstraint(extra_subvertex)
        constrained_subvertex = PartitionedVertex(
            55, 89, get_resources_used_by_atoms(55, 89, []),
            "Constrained vertex", [chip_and_core, same_chip_as_vertex])
        self.subgraph.add_subvertex(constrained_subvertex)
        placement = Placement(constrained_subvertex, 1, 2, 3)
        placement2 = Placement(extra_subvertex, 1, 3, 3)
        placements = Placements([placement, placement2])
        placer = BasicPlacer(self.machine, self.graph)
        constraint = placer._reduce_constraints([same_chip_as_vertex,
                                                 chip_and_core],
                                                constrained_subvertex.label,
                                                placements)

        print constraint.label, 'x:', constraint.x, 'y:', constraint.y, \
            'p:', constraint.p


if __name__ == '__main__':
    unittest.main()
