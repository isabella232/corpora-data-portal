import os
import sys

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".."))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from backend.scripts.create_db import create_db
from backend.corpora.common.utils.db_utils import DbUtils
from backend.corpora.common.corpora_orm import (
    ProjectStatus,
    ProcessingState,
    ValidationState,
    ProjectLinkType,
    DatasetArtifactType,
    DatasetArtifactFileType,
    DbProject,
    DbProjectLink,
    DbDataset,
    DbProjectDataset,
    DbDatasetArtifact,
    DbContributor,
    DbDatasetContributor,
    DbUser,
)


class TestDatabase:
    def __init__(self):
        create_db()
        self.db = DbUtils()
        self._populate_test_data()
        del self.db

    def _populate_test_data(self):
        self._create_test_users()
        self._create_test_projects()
        self._create_test_project_links()
        self._create_test_datasets()
        self._create_test_dataset_artifacts()
        self._create_test_contributors()

    def _create_test_users(self):
        user = DbUser(id="test_user_id", name="test_user", email="test_email")
        self.db.session.add(user)
        self.db.session.commit()

    def _create_test_projects(self):
        project = DbProject(
            id="test_project_id",
            status=ProjectStatus.LIVE.name,
            owner="test_user_id",
            name="test_project",
            description="test_description",
            s3_bucket="test_s3_bucket",
            tc_uri="test_tc_uri",
            needs_attestation=False,
            processing_state=ProcessingState.NA.name,
            validation_state=ValidationState.NOT_VALIDATED.name,
        )
        self.db.session.add(project)
        self.db.session.commit()

    def _create_test_project_links(self):
        project_link = DbProjectLink(
            id="test_project_link_id",
            project_id="test_project_id",
            project_status=ProjectStatus.LIVE.name,
            link_url="test_url",
            link_type=ProjectLinkType.RAW_DATA.name,
        )
        self.db.session.add(project_link)
        self.db.session.commit()

    def _create_test_datasets(self):
        dataset = DbDataset(
            id="test_dataset_id",
            revision=0,
            name="test_dataset_name",
            organism="test_organism",
            organism_ontology="test_organism_ontology",
            tissue="test_tissue",
            tissue_ontology="test_tissue_ontology",
            assay="test_assay",
            assay_ontology="test_assay_ontology",
            disease="test_disease",
            disease_ontology="test_disease_ontology",
            sex="test_sex",
            ethnicity="test_ethnicity",
            ethnicity_ontology="test_ethnicity_ontology",
            source_data_location="test_source_data_location",
            preprint_doi="test_preprint_doi",
            publication_doi="test_publication_doi",
        )
        self.db.session.add(dataset)
        self.db.session.commit()

        project_dataset = DbProjectDataset(
            id="test_project_dataset_id",
            project_id="test_project_id",
            project_status=ProjectStatus.LIVE.name,
            dataset_id="test_dataset_id",
        )
        self.db.session.add(project_dataset)
        self.db.session.commit()

    def _create_test_dataset_artifacts(self):
        dataset_artifact = DbDatasetArtifact(
            id="test_dataset_artifact_id",
            dataset_id="test_dataset_id",
            filename="test_filename",
            filetype=DatasetArtifactFileType.H5AD.name,
            type=DatasetArtifactType.ORIGINAL.name,
            user_submitted=True,
            s3_uri="test_s3_uri",
        )
        self.db.session.add(dataset_artifact)
        self.db.session.commit()

    def _create_test_contributors(self):
        contributor = DbContributor(
            id="test_contributor_id", name="test_contributor_name", institution="test_institution", email="test_email"
        )
        self.db.session.add(contributor)
        self.db.session.commit()

        dataset_contributor = DbDatasetContributor(
            id="test_dataset_contributor_id", contributor_id="test_contributor_id", dataset_id="test_dataset_id"
        )
        self.db.session.add(dataset_contributor)
        self.db.session.commit()