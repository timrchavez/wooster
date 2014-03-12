from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User

from projects.models import (
    Project, DependencyType, Dependency, ProjectDependency, ProjectBuild)
from .factories import ProjectFactory, DependencyFactory, DependencyTypeFactory
from jenkins.tests.factories import JobFactory, BuildFactory, ArtifactFactory


template_config = """
<?xml version='1.0' encoding='UTF-8'?>
<project><description>{{ dependency.description }}</description>
</project>"
"""


class DependencyTypeTest(TestCase):

    def test_instantiation(self):
        """We can create DependencyTypes."""
        dependency_type = DependencyType.objects.create(
            name="my-test", config_xml="testing xml")

    @override_settings(NOTIFICATION_HOST="http://")
    def test_generate_config_for_dependency(self):
        """
        We can use Django templating in the config.xml and this will be
        interpreted correctly.
        """
        dependency_type = DependencyTypeFactory.create(
            name="my-test", config_xml=template_config)
        dependency = DependencyFactory.create()
        job_xml = dependency_type.generate_config_for_dependency(dependency)
        self.assertIn(dependency.description, job_xml)


class DependencyTest(TestCase):

    def test_instantiation(self):
        """We can create Dependencies."""
        dependency_type = DependencyType.objects.create(
            name="my-test", config_xml="testing xml")
        dependency = Dependency.objects.create(
            name="My Dependency", dependency_type=dependency_type)

    def test_get_current_build(self):
        """
        Dependency.get_current_build should return the most recent build that
        has completed and was SUCCESSful.
        """
        build1 = BuildFactory.create()
        build2 = BuildFactory.create(
            phase="FINISHED", result="SUCCESS", job=build1.job)
        dependency = DependencyFactory.create(job=build1.job)
        self.assertEqual(build2, dependency.get_current_build())

    def test_get_current_build_with_no_builds(self):
        """
        If there are no current builds for a given dependency, then we should
        get None.
        """
        dependency = DependencyFactory.create()
        self.assertEqual(None, dependency.get_current_build())


class ProjectDependencyTest(TestCase):

    def test_instantiation(self):
        """We can create ProjectDependency objects."""
        project = ProjectFactory.create()
        dependency = DependencyFactory.create()
        ProjectDependency.objects.create(
            project=project, dependency=dependency)
        self.assertEqual(
            set([dependency]), set(project.dependencies.all()))

    def test_auto_track_build(self):
        """
        If we create a new build for a dependency of a Project, and the
        ProjectDependency is set to auto_track then the current_build should be
        updated to reflect the new build.
        """
        build1 = BuildFactory.create()
        dependency = DependencyFactory.create(job=build1.job)

        project = ProjectFactory.create()
        project_dependency = ProjectDependency.objects.create(
            project=project, dependency=dependency)
        project_dependency.current_build = build1
        project_dependency.save()

        build2 = BuildFactory.create(job=build1.job)
        # Reload the project dependency
        project_dependency = ProjectDependency.objects.get(
            pk=project_dependency.pk)
        self.assertEqual(build2, project_dependency.current_build)

    def test_new_build_with_no_auto_track_build(self):
        """
        If we create a new build for a dependency of a Project, and the
        ProjectDependency is not set to auto_track then the current_build should
        not be updated.
        """
        build1 = BuildFactory.create()
        dependency = DependencyFactory.create(job=build1.job)

        project = ProjectFactory.create()
        project_dependency = ProjectDependency.objects.create(
            project=project, dependency=dependency, auto_track=False)
        project_dependency.current_build = build1
        project_dependency.save()

        build2 = BuildFactory.create(job=build1.job)
        # Reload the project dependency
        project_dependency = ProjectDependency.objects.get(
            pk=project_dependency.pk)
        self.assertEqual(build1, project_dependency.current_build)


class ProjectTest(TestCase):

    def test_get_current_artifacts(self):
        """
        Project.get_current_artifacts returns the current set of artifacts
        for this project.
        """
        project = ProjectFactory.create()
        job = JobFactory.create()
        dependency = DependencyFactory.create(job=job)
        ProjectDependency.objects.create(
            project=project, dependency=dependency)
        build1 = BuildFactory.create(job=job)
        build2 = BuildFactory.create(job=job)

        artifact1 = ArtifactFactory.create(build=build1)
        artifact2 = ArtifactFactory.create(build=build2)

        self.assertEqual([artifact2], list(project.get_current_artifacts()))


class ProjectBuildTest(TestCase):

    def setUp(self):
        self.project = ProjectFactory.create()
        self.user = User.objects.create_user("testing")

    def test_instantiation(self):
        """
        We can create ProjectBuilds.
        """
        project_build = ProjectBuild.objects.create(
            project=self.project, requested_by=self.user)
        self.assertEqual(self.user, project_build.requested_by)
        self.assertIsNotNone(project_build.requested_at)
        self.assertIsNone(project_build.ended_at)
        self.assertEqual("INCOMPLETE", project_build.status)

    def test_create_requirements(self):
        """
        ProjectBuild.create_dependencies has build dependencies with versions
        for each of the dependencies at the time of the call.
        """
        project_build = ProjectBuild.objects.create(
            project=self.project, requested_by=self.user)
        project_build.create_dependencies()
