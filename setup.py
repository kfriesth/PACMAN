try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="SpiNNaker_PACMAN",
    version="3.0.1",
    description="Partition and Configuration Manager",
    url="https://github.com/SpiNNakerManchester/PACMAN",
    license="GNU GPLv3.0",
    packages=['pacman',

              'pacman.executor',
              'pacman.executor.algorithm_classes',
              'pacman.executor.algorithm_decorators',

              'pacman.model',
              'pacman.model.abstract_classes',
              'pacman.model.abstract_classes.impl',
              'pacman.model.constraints',
              'pacman.model.constraints.key_allocator_constraints',
              'pacman.model.constraints.partitioner_constraints',
              'pacman.model.constraints.placer_constraints',
              'pacman.model.constraints.router_constraints',
              'pacman.model.decorators',
              'pacman.model.graphs',
              'pacman.model.graphs.application',
              'pacman.model.graphs.application.impl',
              'pacman.model.graphs.common',
              'pacman.model.graphs.impl',
              'pacman.model.graphs.machine',
              'pacman.model.graphs.machine.impl',
              'pacman.model.placements',
              'pacman.model.resources',
              'pacman.model.routing_info',
              'pacman.model.routing_table_by_partition',
              'pacman.model.routing_tables',
              'pacman.model.tags',

              'pacman.operations',
              'pacman.operations.algorithm_reports',
              'pacman.operations.chip_id_allocator_algorithms',
              'pacman.operations.multi_cast_router_check_functionality',
              'pacman.operations.partition_algorithms',
              'pacman.operations.placer_algorithms',
              'pacman.operations.rig_algorithms',
              'pacman.operations.router_algorithms',
              'pacman.operations.router_compressors',
              'pacman.operations.router_compressors.mundys_router_compressor',
              'pacman.operations.routing_info_allocator_algorithms',
              'pacman.operations.routing_info_allocator_algorithms.field_based_routing_allocator',
              'pacman.operations.routing_info_allocator_algorithms.malloc_based_routing_allocator',
              'pacman.operations.routing_table_generators',
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
        'six', 'enum34', 'numpy', 'jsonschema', 'rig >= 2.0.0, < 3.0.0',
        'SpiNNMachine >= 3.0.0, < 4.0.0']
)
