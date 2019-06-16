""" Class for downloading and loading required external resources.

`lineage` uses tables and data from UCSC's Genome Browser:

* http://genome.ucsc.edu/
* http://genome.ucsc.edu/cgi-bin/hgTables

References
----------
..[1] Karolchik D, Hinrichs AS, Furey TS, Roskin KM, Sugnet CW, Haussler D, Kent WJ.
  The UCSC Table Browser data retrieval tool. Nucleic Acids Res. 2004 Jan
  1;32(Database issue):D493-6. PubMed PMID: 14681465; PubMed Central PMCID:
  PMC308837. https://www.ncbi.nlm.nih.gov/pubmed/14681465
..[2] Tyner C, Barber GP, Casper J, Clawson H, Diekhans M, Eisenhart C, Fischer CM,
  Gibson D, Gonzalez JN, Guruvadoo L, Haeussler M, Heitner S, Hinrichs AS,
  Karolchik D, Lee BT, Lee CM, Nejad P, Raney BJ, Rosenbloom KR, Speir ML,
  Villarreal C, Vivian J, Zweig AS, Haussler D, Kuhn RM, Kent WJ. The UCSC Genome
  Browser database: 2017 update. Nucleic Acids Res. 2017 Jan 4;45(D1):D626-D634.
  doi: 10.1093/nar/gkw1134. Epub 2016 Nov 29. PubMed PMID: 27899642; PubMed Central
  PMCID: PMC5210591. https://www.ncbi.nlm.nih.gov/pubmed/27899642
..[3] International Human Genome Sequencing Consortium. Initial sequencing and
  analysis of the human genome. Nature. 2001 Feb 15;409(6822):860-921.
  http://dx.doi.org/10.1038/35057062
..[4] hg19 (GRCh37): Hiram Clawson, Brooke Rhead, Pauline Fujita, Ann Zweig, Katrina
  Learned, Donna Karolchik and Robert Kuhn, https://genome.ucsc.edu/cgi-bin/hgGateway?db=hg19
..[5] Yates et. al. (doi:10.1093/bioinformatics/btu613),
  http://europepmc.org/search/?query=DOI:10.1093/bioinformatics/btu613
..[6] Zerbino et. al. (doi.org/10.1093/nar/gkx1098), https://doi.org/10.1093/nar/gkx1098

"""

"""
Copyright (C) 2017 Andrew Riha

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import itertools
import tarfile
import zlib

from atomicwrites import atomic_write
import pandas as pd
from snps import Resources as SNPsResources


class Resources(SNPsResources):
    """ Object used to manage resources required by `lineage`. """

    def __init__(self, resources_dir="resources"):
        """ Initialize a ``Resources`` object.

        Parameters
        ----------
        resources_dir : str
            name / path of resources directory
        """
        super().__init__(resources_dir=resources_dir)

        self._genetic_map_HapMapII_GRCh37 = {}
        self._cytoBand_hg19 = pd.DataFrame()
        self._knownGene_hg19 = pd.DataFrame()
        self._kgXref_hg19 = pd.DataFrame()

    def get_genetic_map_HapMapII_GRCh37(self):
        """ Get International HapMap Consortium HapMap Phase II genetic map for Build 37.

        Returns
        -------
        dict
            dict of pandas.DataFrame HapMapII genetic maps if loading was successful, else {}
        """
        if not self._genetic_map_HapMapII_GRCh37:
            self._genetic_map_HapMapII_GRCh37 = self._load_genetic_map(
                self._get_path_genetic_map_HapMapII_GRCh37()
            )

        return self._genetic_map_HapMapII_GRCh37

    def get_cytoBand_hg19(self):
        """ Get UCSC cytoBand table for Build 37.

        Returns
        -------
        pandas.DataFrame
            cytoBand table if loading was successful, else empty DataFrame
        """
        if self._cytoBand_hg19.empty:
            self._cytoBand_hg19 = self._load_cytoBand(self._get_path_cytoBand_hg19())

        return self._cytoBand_hg19

    def get_knownGene_hg19(self):
        """ Get UCSC knownGene table for Build 37.

        Returns
        -------
        pandas.DataFrame
            knownGene table if loading was successful, else empty DataFrame
        """
        if self._knownGene_hg19.empty:
            self._knownGene_hg19 = self._load_knownGene(self._get_path_knownGene_hg19())

        return self._knownGene_hg19

    def get_kgXref_hg19(self):
        """ Get UCSC kgXref table for Build 37.

        Returns
        -------
        pandas.DataFrame
            kgXref table if loading was successful, else empty DataFrame
        """
        if self._kgXref_hg19.empty:
            self._kgXref_hg19 = self._load_kgXref(self._get_path_kgXref_hg19())

        return self._kgXref_hg19

    def download_example_datasets(self):
        """ Download example datasets from `openSNP <https://opensnp.org>`_.

        Per openSNP, "the data is donated into the public domain using `CC0 1.0
        <http://creativecommons.org/publicdomain/zero/1.0/>`_."

        Returns
        -------
        paths : list of str or empty str
            paths to example datasets

        References
        ----------
        ..[1] Greshake B, Bayer PE, Rausch H, Reda J (2014), "openSNP-A Crowdsourced Web Resource
          for Personal Genomics," PLOS ONE, 9(3): e89204,
          https://doi.org/10.1371/journal.pone.0089204
        """
        paths = []
        paths.append(
            self._download_file(
                "https://opensnp.org/data/662.23andme.304",
                "662.23andme.304.txt.gz",
                compress=True,
            )
        )
        paths.append(
            self._download_file(
                "https://opensnp.org/data/662.23andme.340",
                "662.23andme.340.txt.gz",
                compress=True,
            )
        )
        paths.append(
            self._download_file(
                "https://opensnp.org/data/662.ftdna-illumina.341",
                "662.ftdna-illumina.341.csv.gz",
                compress=True,
            )
        )
        paths.append(
            self._download_file(
                "https://opensnp.org/data/663.23andme.305",
                "663.23andme.305.txt.gz",
                compress=True,
            )
        )

        # these two files consist of concatenated gzip files and therefore need special handling
        paths.append(
            self._download_file(
                "https://opensnp.org/data/4583.ftdna-illumina.3482",
                "4583.ftdna-illumina.3482.csv.gz",
            )
        )
        paths.append(
            self._download_file(
                "https://opensnp.org/data/4584.ftdna-illumina.3483",
                "4584.ftdna-illumina.3483.csv.gz",
            )
        )

        try:
            for gzip_path in paths[-2:]:
                # https://stackoverflow.com/q/4928560
                # https://stackoverflow.com/a/37042747
                with open(gzip_path, "rb") as f:
                    decompressor = zlib.decompressobj(31)

                    # decompress data from first concatenated gzip file
                    data = decompressor.decompress(f.read())

                    if len(decompressor.unused_data) > 0:
                        # decompress data from second concatenated gzip file, if any
                        additional_data = zlib.decompress(decompressor.unused_data, 31)
                        data += additional_data[33:]  # skip over second header

                # recompress data
                with atomic_write(gzip_path, mode="wb", overwrite=True) as f:
                    self._write_data_to_gzip(f, data)
        except Exception as err:
            print(err)

        return paths

    def get_all_resources(self):
        """ Get / download all resources (except reference sequences) used throughout `lineage`.

        Returns
        -------
        dict
            dict of resources
        """
        resources = {}
        resources[
            "genetic_map_HapMapII_GRCh37"
        ] = self.get_genetic_map_HapMapII_GRCh37()
        resources["cytoBand_hg19"] = self.get_cytoBand_hg19()
        resources["knownGene_hg19"] = self.get_knownGene_hg19()
        resources["kgXref_hg19"] = self.get_kgXref_hg19()
        for source, target in itertools.permutations(["NCBI36", "GRCh37", "GRCh38"], 2):
            resources[source + "_" + target] = self.get_assembly_mapping_data(
                source, target
            )
        return resources

    @staticmethod
    def _load_genetic_map(filename):
        """ Load genetic map (e.g. HapMapII).

        Parameters
        ----------
        filename : str
            path to compressed archive with genetic map data

        Returns
        -------
        genetic_map : dict
            dict of pandas.DataFrame genetic maps if loading was successful, else {}

        Notes
        -----
        Keys of returned dict are chromosomes and values are the corresponding genetic map.
        """
        try:
            genetic_map = {}

            with tarfile.open(filename, "r") as tar:
                # http://stackoverflow.com/a/2018576
                for member in tar.getmembers():
                    if "genetic_map" in member.name:
                        df = pd.read_csv(tar.extractfile(member), sep="\t")
                        df = df.rename(
                            columns={
                                "Position(bp)": "pos",
                                "Rate(cM/Mb)": "rate",
                                "Map(cM)": "map",
                            }
                        )
                        del df["Chromosome"]
                        start_pos = member.name.index("chr") + 3
                        end_pos = member.name.index(".")
                        genetic_map[member.name[start_pos:end_pos]] = df

            # X chrom consists of X PAR regions and X non-PAR region
            genetic_map["X"] = pd.concat(
                [genetic_map["X_par1"], genetic_map["X"], genetic_map["X_par2"]]
            )
            del genetic_map["X_par1"]
            del genetic_map["X_par2"]

            return genetic_map
        except Exception as err:
            print(err)
            return {}

    @staticmethod
    def _load_cytoBand(filename):
        """ Load UCSC cytoBand table.

        Parameters
        ----------
        filename : str
            path to cytoBand file

        Returns
        -------
        df : pandas.DataFrame
            cytoBand table if loading was successful, else empty DataFrame

        References
        ----------
        ..[1] Ryan Dale, GitHub Gist,
          https://gist.github.com/daler/c98fc410282d7570efc3#file-ideograms-py
        """
        try:
            # adapted from chromosome plotting code (see [1]_)
            df = pd.read_csv(
                filename, names=["chrom", "start", "end", "name", "gie_stain"], sep="\t"
            )
            df["chrom"] = df["chrom"].str[3:]
            return df
        except Exception as err:
            print(err)
            return pd.DataFrame()

    @staticmethod
    def _load_knownGene(filename):
        """ Load UCSC knownGene table.

        Parameters
        ----------
        filename : str
            path to knownGene file

        Returns
        -------
        df : pandas.DataFrame
            knownGene table if loading was successful, else empty DataFrame
        """
        try:
            df = pd.read_csv(
                filename,
                names=[
                    "name",
                    "chrom",
                    "strand",
                    "txStart",
                    "txEnd",
                    "cdsStart",
                    "cdsEnd",
                    "exonCount",
                    "exonStarts",
                    "exonEnds",
                    "proteinID",
                    "alignID",
                ],
                index_col=0,
                sep="\t",
            )
            df["chrom"] = df["chrom"].str[3:]
            return df
        except Exception as err:
            print(err)
            return pd.DataFrame()

    @staticmethod
    def _load_kgXref(filename):
        """ Load UCSC kgXref table.

        Parameters
        ----------
        filename : str
            path to kgXref file

        Returns
        -------
        df : pandas.DataFrame
            kgXref table if loading was successful, else empty DataFrame
        """
        try:
            df = pd.read_csv(
                filename,
                names=[
                    "kgID",
                    "mRNA",
                    "spID",
                    "spDisplayID",
                    "geneSymbol",
                    "refseq",
                    "protAcc",
                    "description",
                    "rfamAcc",
                    "tRnaName",
                ],
                index_col=0,
                sep="\t",
                dtype=object,
            )
            return df
        except Exception as err:
            print(err)
            return pd.DataFrame()

    def _get_path_cytoBand_hg19(self):
        """ Get local path to cytoBand file for hg19 / GRCh37 from UCSC, downloading if necessary.

        Returns
        -------
        str
            path to cytoBand_hg19.txt.gz
        """
        return self._download_file(
            "ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/cytoBand.txt.gz",
            "cytoBand_hg19.txt.gz",
        )

    def _get_path_genetic_map_HapMapII_GRCh37(self):
        """ Get local path to HapMap Phase II genetic map for hg19 / GRCh37 (HapMapII),
        downloading if necessary.

        Returns
        -------
        str
            path to genetic_map_HapMapII_GRCh37.tar.gz

        References
        ----------
        ..[1] "The International HapMap Consortium (2007).  A second generation human haplotype
          map of over 3.1 million SNPs.  Nature 449: 851-861."
        ..[2] "The map was generated by lifting the HapMap Phase II genetic map from build 35 to
          GRCh37. The original map was generated using LDhat as described in the 2007 HapMap
          paper (Nature, 18th Sept 2007). The conversion from b35 to GRCh37 was achieved using
          the UCSC liftOver tool. Adam Auton, 08/12/2010"
        """
        return self._download_file(
            "ftp://ftp.ncbi.nlm.nih.gov/hapmap/recombination/2011-01_phaseII_B37/"
            "genetic_map_HapMapII_GRCh37.tar.gz",
            "genetic_map_HapMapII_GRCh37.tar.gz",
        )

    def _get_path_knownGene_hg19(self):
        """ Get local path to knownGene file for hg19 / GRCh37 from UCSC, downloading if necessary.

        Returns
        -------
        str
            path to knownGene_hg19.txt.gz
        """
        return self._download_file(
            "ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/knownGene.txt.gz",
            "knownGene_hg19.txt.gz",
        )

    def _get_path_kgXref_hg19(self):
        """ Get local path to kgXref file for hg19 / GRCh37 from UCSC, downloading if necessary.

        Returns
        -------
        str
            path to kgXref_hg19.txt.gz
        """
        return self._download_file(
            "ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/kgXref.txt.gz",
            "kgXref_hg19.txt.gz",
        )
