"""
Database router for multi-school multi-database support.
Routes database queries to the appropriate database based on school selection.
"""
from threading import local
from django.conf import settings

# Thread-local storage for database context
_thread_local = local()


class SchoolDatabaseRouter:
    """
    A router to control database operations on models based on school selection.
    """

    def db_for_read(self, model, **hints):
        """
        Direct read operations to the appropriate database based on selected school.
        """
        return self.get_db_for_school()

    def db_for_write(self, model, **hints):
        """
        Direct write operations to the appropriate database based on selected school.
        """
        return self.get_db_for_school()

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects in the same database.
        """
        db1 = self.get_db_for_school()
        db2 = self.get_db_for_school()
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations run on the primary database.
        """
        return db == 'default'

    @staticmethod
    def get_db_for_school():
        """
        Get the database name for the current school context.
        Returns 'default' (Erp_Database) for School 1
        Returns 'secondary' (Erp_Database2) for School 2
        """
        school_id = getattr(_thread_local, 'school_id', None)

        if school_id == 'school2':
            return 'secondary'

        # Default to primary database for School 1
        return 'default'

    @staticmethod
    def set_school(school_id):
        """
        Set the current school context for database operations.

        Args:
            school_id: 'school1' or 'school2'
        """
        _thread_local.school_id = school_id

    @staticmethod
    def get_current_school():
        """
        Get the currently selected school.
        """
        return getattr(_thread_local, 'school_id', 'school1')

    @staticmethod
    def clear_school():
        """
        Clear the school context.
        """
        if hasattr(_thread_local, 'school_id'):
            del _thread_local.school_id
