# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from lms.models.assignment_model import StudentAssignment
from lms.models.course_model import Course
from lms.tables import StudentAssignmentTable, StudentAssignmentFilter


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "lms/course/home.html"


class GradeBookCourseView(LoginRequiredMixin, UserPassesTestMixin, ExportMixin, SingleTableMixin, FilterView):
    model = StudentAssignment
    table_class = StudentAssignmentTable
    # queryset = StudentAssignment.objects.filter(assignment__for_course__id=6)
    template_name = 'lms/course/gradebook/course_gradebook.html'
    filterset_class = StudentAssignmentFilter

    def get_queryset(self):
        return StudentAssignment.objects.filter(assignment__for_course__id=self.kwargs['course_id'])

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user.role.is_teacher:
            return True
        elif self.request.user.role.is_teaching_assistant:
            return True
        return False

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


