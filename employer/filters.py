import django_filters
from employer.models import Jobs


class PostedJobFilter(django_filters.FilterSet):
    salary = django_filters.NumberFilter(field_name='salary', lookup_expr='lt')
    job_title = django_filters.CharFilter(field_name='job_title', lookup_expr='contains')
    class Meta:
        model=Jobs
        fields=[
            'posted_by',
            'job_title',
            'role',
            'location',
            'salary',
            'qulaification'
        ]