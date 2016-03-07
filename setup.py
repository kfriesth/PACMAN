try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="SpiNNaker_PACMAN",
    version="2016.001",
    description="Partition and Configuration Manager",
    url="https://github.com/SpiNNakerManchester/PACMAN",
    license="GNU GPLv3.0",
    packages=['pacman',
              'pacman.interfaces',
              'pacman.model',
              'pacman.model.abstract_classes',
              'pacman.model.constraints',
              'pacman.model.constraints.abstract_constraints',
              'pacman.model.constraints.key_allocator_constraints',
              'pacman.model.constraints.partitioner_constraints',
              'pacman.model.constraints.placer_constraints',
              'pacman.model.constraints.tag_allocator_constraints',
              'pacman.model.data_request_interfaces',
              'pacman.model.graph_mapper',
              'pacman.model.partitionable_graph',
              'pacman.model.partitioned_graph',
              'pacman.model.placements',
              'pacman.model.resources',
              'pacman.model.routing_info',
              'pacman.model.routing_tables',
              'pacman.model.tags',
              'pacman.operations',
              'pacman.operations.algorithm_reports',
              'pacman.operations.chip_id_allocator_algorithms',
              'pacman.operations.multi_cast_router_check_functionality',
              'pacman.operations.partition_algorithms',
              'pacman.operations.placer_algorithms',
              'pacman.operations.router_algorithms',
              'pacman.operations.routing_info_allocator_algorithms',
              'pacman.operations.routing_info_allocator_algorithms.malloc_based_routing_allocator',
              'pacman.operations.tag_allocator_algorithms',
              'pacman.utilities',
              'pacman.utilities.algorithm_utilities',
              'pacman.utilities.file_format_converters',
              'pacman.utilities.file_format_schemas',
              'pacman.utilities.utility_objs'],
    package_data={'pacman.operations.algorithm_reports': ['*.xml'],
                  'pacman.operations': ['*.xml', '*.xsd'],
                  'pacman.utilities.file_format_converters': ['*.xml'],
                  'pacman.utilities.file_format_schemas': ['*.json']},
    install_requires=[
        'six', 'enum34', 'numpy', 'jsonschema', 'SpiNNMan==2016.001',
        'SpiNNMachine==2015.004.01'],
    dependency_links=['https://github.com/SpiNNakerManchester/SpiNNMan/tarball/master#egg=SpiNNMan-2016.001', 
                      'https://github.com/SpiNNakerManchester/SpiNNMachine/tarball/master#egg=SpiNNMachine-2015.004.01']
)
