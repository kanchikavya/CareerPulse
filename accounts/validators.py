import os
from django.core.exceptions import ValidationError

def validate_pdf_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError('Only PDF files are allowed for resume upload.')

def validate_file_size(value):
    max_size_mb = 5
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size must not exceed {max_size_mb} MB.')
