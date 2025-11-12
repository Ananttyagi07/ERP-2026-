"""Library Management models"""
from django.db import models
from apps.core.models import TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel


class Book(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Physical books in library"""
    title = models.CharField(max_length=255)
    book_id = models.CharField(max_length=100, unique=True)
    isbn_no = models.CharField(max_length=50, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    almira_no = models.CharField(max_length=50, blank=True)
    book_cover = models.ImageField(upload_to='library/books/', null=True, blank=True)

    class Meta:
        db_table = 'library_books'

    def __str__(self):
        return f"{self.title} ({self.book_id})"


class LibraryMember(TimeStampedModel, CollegeIsolatedModel):
    """Library membership for students"""
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='library_membership')
    library_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'library_members'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.library_id}"


class BookIssue(TimeStampedModel, CollegeIsolatedModel):
    """Book issue/return records"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    member = models.ForeignKey(LibraryMember, on_delete=models.CASCADE, related_name='book_issues')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'book_issues'

    def __str__(self):
        return f"{self.book.title} - {self.member.student.user.get_full_name()}"


class EBook(TimeStampedModel, CollegeIsolatedModel, SoftDeleteModel):
    """Digital books/documents"""
    school_class = models.ForeignKey('academic.SchoolClass', on_delete=models.CASCADE)
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    edition = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=100, blank=True)
    cover_image = models.ImageField(upload_to='library/ebook_covers/', null=True, blank=True)
    ebook_file = models.FileField(upload_to='library/ebooks/')

    class Meta:
        db_table = 'ebooks'

    def __str__(self):
        return self.name
