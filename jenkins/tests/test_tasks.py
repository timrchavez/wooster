import logging

from django.test import TestCase
from django.test.utils import override_settings

import mock

from jenkins.tasks import build_job, push_job_to_jenkins
from jenkins.models import JenkinsServer
from .factories import (
    JobFactory, JenkinsServerFactory, BuildFactory, JobTypeFactory)


class BuildJobTaskTest(TestCase):

    def setUp(self):
        self.server = JenkinsServerFactory.create()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_build_job(self):
        """
        The build_job task should find the associated server, and request that
        the job be built.
        """
        job = JobFactory.create(server=self.server)
        with mock.patch("jenkins.models.Jenkins", spec=True) as mock_jenkins:
            build_job(job.pk)

        mock_jenkins.assert_called_with(
            self.server.url, username=u"root", password=u"testing")
        mock_jenkins.return_value.build_job.assert_called_with(
            job.name, params={})

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_build_job_with_build_id(self):
        """
        If we provide a build_id, this should be sent as parameter.
        """
        job = JobFactory.create(server=self.server)
        with mock.patch("jenkins.models.Jenkins", spec=True) as mock_jenkins:
            build_job(job.pk, "20140312.1")

        mock_jenkins.assert_called_with(
            self.server.url, username=u"root", password=u"testing")
        mock_jenkins.return_value.build_job.assert_called_with(
            job.name, params={"BUILD_ID": "20140312.1"})


class ImportBuildTaskTest(TestCase):
    # TODO: This needs written...
    pass


job_xml = """
<?xml version='1.0' encoding='UTF-8'?>
<project>{{ notifications_url }}</project>
"""


class CreateJobTaskTest(TestCase):

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_push_job_to_jenkins(self):
        """
        The push_job_to_jenkins task should find the associated server, and
        create the job with the right name and content.
        """
        jobtype = JobTypeFactory.create(config_xml=job_xml)
        job = JobFactory.create(jobtype=jobtype)
        with mock.patch("jenkins.models.Jenkins", spec=True) as mock_jenkins:
            push_job_to_jenkins(job.pk)

        mock_jenkins.assert_called_with(
            job.server.url, username=u"root", password=u"testing")
        mock_jenkins.return_value.create_job.assert_called_with(
            job.name, job.jobtype.config_xml)
