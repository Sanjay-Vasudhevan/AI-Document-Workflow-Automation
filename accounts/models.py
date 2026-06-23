from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends Django's built-in User model with business-specific
    attributes required by the workflow system — primarily the
    user's role, which drives permissions and dashboard routing
    throughout the application.
    """

    ROLE_EMPLOYEE = 'EMPLOYEE'
    ROLE_MANAGER = 'MANAGER'
    ROLE_ADMIN = 'ADMIN'

    ROLE_CHOICES = [
        (ROLE_EMPLOYEE, 'Employee'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_EMPLOYEE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_employee(self):
        return self.role == self.ROLE_EMPLOYEE

    @property
    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    @property
    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN