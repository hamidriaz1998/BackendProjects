from typing import Dict, Type

from .email_types import EmailType
from .templates.email_base import EmailBase


class TemplateRegistry:
    """Registry for email templates that allows automatic registration and creation."""

    _templates: Dict[EmailType, Type[EmailBase]] = {}

    @classmethod
    def register(cls, email_type: EmailType, template_class: Type[EmailBase]):
        """Register a template class for a specific email type."""
        cls._templates[email_type] = template_class

    @classmethod
    def get_template_class(cls, email_type: EmailType) -> Type[EmailBase]:
        """Get the template class for a specific email type."""
        if email_type not in cls._templates:
            raise ValueError(f"No template registered for email type: {email_type}")
        return cls._templates[email_type]

    @classmethod
    def create_template(cls, email_type: EmailType, **kwargs) -> EmailBase:
        """Create a template instance for the given email type with provided kwargs."""
        template_class = cls.get_template_class(email_type)

        # Validate arguments before creating the template
        template_class.check_args(kwargs)

        return template_class(**kwargs)

    @classmethod
    def get_registered_types(cls) -> list[EmailType]:
        """Get all registered email types."""
        return list(cls._templates.keys())

    @classmethod
    def is_registered(cls, email_type: EmailType) -> bool:
        """Check if an email type is registered."""
        return email_type in cls._templates


# Process any pending registrations from decorators
def _initialize_registrations():
    """Initialize all pending template registrations."""
    try:
        from .decorators import _process_pending_registrations

        _process_pending_registrations()
    except ImportError:
        # decorators module not available yet
        pass


# Call initialization when module is loaded
_initialize_registrations()
