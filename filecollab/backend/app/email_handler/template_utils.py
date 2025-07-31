from .email_types import EmailType
from .template_registry import TemplateRegistry


def list_registered_templates() -> dict:
    """
    Utility function to list all registered email templates.
    Useful for debugging and documentation.
    """
    registered = {}
    for email_type in TemplateRegistry.get_registered_types():
        template_class = TemplateRegistry.get_template_class(email_type)
        registered[email_type.value] = {
            "class_name": template_class.__name__,
            "module": template_class.__module__,
        }
    return registered


def validate_template_args(email_type: EmailType, **kwargs) -> bool:
    """
    Validate arguments for a specific email type without creating the template.
    Returns True if valid, raises ValueError if invalid.
    """
    try:
        template_class = TemplateRegistry.get_template_class(email_type)
        template_class.check_args(kwargs)
        return True
    except ValueError:
        raise
