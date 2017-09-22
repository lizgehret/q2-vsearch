# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import skbio
import biom
import numpy as np
import tempfile

from qiime2.plugin.testing import TestPluginBase
from qiime2.util import redirected_stdio
from q2_types.feature_data import DNAFASTAFormat

from q2_vsearch._cluster_features import (cluster_features_denovo,
                                          _fasta_with_sizes)


class ClusterFeaturesDenovoTests(TestPluginBase):

    package = 'q2_vsearch.tests'

    def test_no_clustering(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[100, 101, 103],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        with redirected_stdio(stderr=os.devnull):
            obs_table, obs_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=1.0)
        # order of identifiers is important for biom.Table equality
        obs_table = \
            obs_table.sort_order(input_table.ids(axis='observation'),
                                 axis='observation')
        self.assertEqual(obs_table, input_table)

        obs_seqs = list(skbio.io.read(str(obs_sequences),
                                      constructor=skbio.DNA, format='fasta'))
        exp_seqs = list(skbio.io.read(str(input_sequences),
                                      constructor=skbio.DNA, format='fasta'))

        # sequences are reverse-sorted by abundance in output
        exp_seqs = [exp_seqs[0], exp_seqs[3], exp_seqs[2], exp_seqs[1]]
        self.assertEqual(obs_seqs, exp_seqs)

    def test_99_percent_clustering(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[100, 101, 103],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        exp_table = biom.Table(np.array([[104, 106, 109],
                                         [1, 1, 2],
                                         [7, 8, 9]]),
                               ['feature1', 'feature2',
                                'feature4'],
                               ['sample1', 'sample2', 'sample3'])

        with redirected_stdio(stderr=os.devnull):
            obs_table, obs_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=0.99)
        # order of identifiers is important for biom.Table equality
        obs_table = \
            obs_table.sort_order(exp_table.ids(axis='observation'),
                                 axis='observation')
        self.assertEqual(obs_table, exp_table)

        # sequences are reverse-sorted by abundance in output
        obs_seqs = list(skbio.io.read(str(obs_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = list(skbio.io.read(str(input_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = [exp_seqs[0], exp_seqs[3], exp_seqs[1]]
        self.assertEqual(obs_seqs, exp_seqs)

    def test_97_percent_clustering(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[100, 101, 103],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        exp_table = biom.Table(np.array([[111, 114, 118],
                                         [1, 1, 2]]),
                               ['feature1', 'feature2'],
                               ['sample1', 'sample2', 'sample3'])

        with redirected_stdio(stderr=os.devnull):
            obs_table, obs_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=0.97)
        # order of identifiers is important for biom.Table equality
        obs_table = \
            obs_table.sort_order(exp_table.ids(axis='observation'),
                                 axis='observation')
        self.assertEqual(obs_table, exp_table)

        # sequences are reverse-sorted by abundance in output
        obs_seqs = list(skbio.io.read(str(obs_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = list(skbio.io.read(str(input_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = [exp_seqs[0], exp_seqs[1]]
        self.assertEqual(obs_seqs, exp_seqs)

    def test_97_percent_clustering_feature3_most_abundant(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[4, 5, 6],
                                           [1, 1, 2],
                                           [100, 101, 103],
                                           [7, 8, 9]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        exp_table = biom.Table(np.array([[111, 114, 118],
                                         [1, 1, 2]]),
                               ['feature3', 'feature2'],
                               ['sample1', 'sample2', 'sample3'])

        with redirected_stdio(stderr=os.devnull):
            obs_table, obs_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=0.97)
        # order of identifiers is important for biom.Table equality
        obs_table = \
            obs_table.sort_order(exp_table.ids(axis='observation'),
                                 axis='observation')
        self.assertEqual(obs_table, exp_table)

        # sequences are reverse-sorted by abundance in output
        obs_seqs = list(skbio.io.read(str(obs_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = list(skbio.io.read(str(input_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = [exp_seqs[2], exp_seqs[1]]
        self.assertEqual(obs_seqs, exp_seqs)

    def test_97_percent_clustering_feature4_most_abundant(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[4, 5, 6],
                                           [1, 1, 2],
                                           [7, 8, 9],
                                           [100, 101, 103]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        exp_table = biom.Table(np.array([[111, 114, 118],
                                         [1, 1, 2]]),
                               ['feature4', 'feature2'],
                               ['sample1', 'sample2', 'sample3'])

        with redirected_stdio(stderr=os.devnull):
            obs_table, obs_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=0.97)
        # order of identifiers is important for biom.Table equality
        obs_table = \
            obs_table.sort_order(exp_table.ids(axis='observation'),
                                 axis='observation')
        self.assertEqual(obs_table, exp_table)

        # sequences are reverse-sorted by abundance in output
        obs_seqs = list(skbio.io.read(str(obs_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = list(skbio.io.read(str(input_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = [exp_seqs[3], exp_seqs[1]]
        self.assertEqual(obs_seqs, exp_seqs)

    def test_1_percent_clustering(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[100, 101, 103],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        exp_table = biom.Table(np.array([[112, 115, 120]]),
                               ['feature1'],
                               ['sample1', 'sample2', 'sample3'])

        with redirected_stdio(stderr=os.devnull):
            obs_table, obs_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=0.01)
        # order of identifiers is important for biom.Table equality
        obs_table = \
            obs_table.sort_order(exp_table.ids(axis='observation'),
                                 axis='observation')
        self.assertEqual(obs_table, exp_table)

        # sequences are reverse-sorted by abundance in output
        obs_seqs = list(skbio.io.read(str(obs_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = list(skbio.io.read(str(input_sequences),
                        constructor=skbio.DNA, format='fasta'))
        exp_seqs = [exp_seqs[0]]
        self.assertEqual(obs_seqs, exp_seqs)

    def test_extra_features_in_sequences(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[0, 1, 3], [1, 1, 2], [4, 5, 6]]),
                                 ['feature1', 'feature2', 'feature3'],
                                 ['sample1', 'sample2', 'sample3'])
        with self.assertRaisesRegex(ValueError,
                                    expected_regex='Feature feature4 is pre'):
            clustered_table, clustered_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=1.0)

    def test_extra_features_in_table(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[0, 1, 3],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9],
                                           [1, 1, 1]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4', 'feature5'],
                                 ['sample1', 'sample2', 'sample3'])
        with self.assertRaisesRegex(ValueError,
                                    expected_regex='Some feat.*feature5.*'):
            clustered_table, clustered_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=1.0)

    def test_no_overlapping_feature_ids(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_sequences = DNAFASTAFormat(input_sequences_fp, mode='r')
        input_table = biom.Table(np.array([[0, 1, 3],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9],
                                           [1, 1, 1]]),
                                 ['f1', 'f2', 'f3',
                                  'f4', 'f5'],
                                 ['sample1', 'sample2', 'sample3'])
        with self.assertRaisesRegex(ValueError,
                                    expected_regex='Feature feature1 is pre'):
            clustered_table, clustered_sequences = cluster_features_denovo(
                sequences=input_sequences, table=input_table,
                perc_identity=1.0)


class PrivateFunctionTests(TestPluginBase):

    package = 'q2_vsearch.tests'

    def test_fasta_with_sizes(self):
        input_sequences_fp = self.get_data_path('dna-sequences-1.fasta')
        input_table = biom.Table(np.array([[100, 101, 103],
                                           [1, 1, 2],
                                           [4, 5, 6],
                                           [7, 8, 9]]),
                                 ['feature1', 'feature2', 'feature3',
                                  'feature4'],
                                 ['sample1', 'sample2', 'sample3'])
        with tempfile.NamedTemporaryFile() as output_sequences_f:
            _fasta_with_sizes(input_sequences_fp,
                              output_sequences_f.name,
                              input_table)

            obs_seqs = list(skbio.io.read(output_sequences_f.name,
                                          constructor=skbio.DNA,
                                          format='fasta'))
            input_seqs = list(skbio.io.read(input_sequences_fp,
                                            constructor=skbio.DNA,
                                            format='fasta'))

            self.assertEqual(len(obs_seqs), len(input_seqs))

            self.assertEqual(obs_seqs[0].metadata['id'], 'feature1;size=304')
            self.assertEqual(str(obs_seqs[0]), str(input_seqs[0]))
            self.assertEqual(obs_seqs[1].metadata['id'], 'feature2;size=4')
            self.assertEqual(str(obs_seqs[1]), str(input_seqs[1]))
            self.assertEqual(obs_seqs[2].metadata['id'], 'feature3;size=15')
            self.assertEqual(str(obs_seqs[2]), str(input_seqs[2]))
            self.assertEqual(obs_seqs[3].metadata['id'], 'feature4;size=24')
            self.assertEqual(str(obs_seqs[3]), str(input_seqs[3]))
