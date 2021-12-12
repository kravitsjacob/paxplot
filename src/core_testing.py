"""Tests for core parapy functions"""

import unittest

import core


class AnalysisLib(unittest.TestCase):
    def test_parallel_basic(self):
        """
        Basic test of parallel functionality
        """
        # Setup
        data = [
            {'A': 0.0, 'B': 0.0, 'C': 0.0},
            {'A': 1.0, 'B': 1.0, 'C': 1.0},
            {'A': 2.0, 'B': 2.0, 'C': 2.0},
        ]

        # Run
        fig = core.parallel(data=data, cols=['A', 'B', 'C'])
        fig.show()

    def test_parallel_subset_columns(self):
        """
        Testing plotting a subset of all the columns
        """
        # Setup
        data = [
            {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0},
            {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0},
            {'A': 2.0, 'B': 2.0, 'C': 2.0, 'D': 2.0},
        ]

        # Run
        fig = core.parallel(data=data, cols=['A', 'C', 'D'])
        fig.show()

    def test_parallel_subset_columns_different(self):
        """
        Testing plotting a subset of all the columns with different values
        """
        # Setup
        data = [
            {'A': 0.0, 'B': 1.0, 'C': 0.0, 'D': 2.0},
            {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0},
            {'A': 2.0, 'B': 1.0, 'C': 2.0, 'D': 0.0},
        ]

        # Run
        fig = core.parallel(data=data, cols=['A', 'B', 'D'])
        fig.show()

    def test_parallel_subset_last_column_large(self):
        """
        Testing plotting a subset of all the columns with different values
        """
        # Setup
        data = [
            {'A': 0.0, 'B': 1.0, 'C': 0.0, 'D': 3.0},
            {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0},
            {'A': 2.0, 'B': 1.0, 'C': 2.0, 'D': 0.0},
        ]

        # Run
        fig = core.parallel(data=data, cols=['A', 'B', 'D'])
        fig.show()

    def test_parallel_limits(self):
        """
        Testing plotting a subset of all the columns with different values
        """
        # Setup
        data = [
            {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0},
            {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0},
            {'A': 2.0, 'B': 2.0, 'C': 2.0, 'D': 2.0},
        ]
        cols = ['A', 'B', 'D']
        custom_lims = {
            'A': [0, 10],
            'B': [0, 1],
            'D': [0, 5]
        }

        # Run
        fig = core.parallel(
            data=data,
            cols=cols,
            custom_lims=custom_lims
        )
        fig.show()


if __name__ == '__main__':
    unittest.main()
