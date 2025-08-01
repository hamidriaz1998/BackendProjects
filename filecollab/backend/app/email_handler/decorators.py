from typing import List, Tuple, Type

from .email_types import EmailType

# Store pending registrations until TemplateRegistry is available
_pending_registrations: List[Tuple[EmailType, Type]] = []


def register_template(email_type: EmailType):
    """Decorator to automatically register email templates."""

    def decorator(template_class: Type):
        _pending_registrations.append((email_type, template_class))
        return template_class

    return decorator


def _process_pending_registrations():
    """Process all pending registrations. Called when TemplateRegistry is ready."""
    from .template_registry import TemplateRegistry

    for email_type, template_class in _pending_registrations:
        TemplateRegistry.register(email_type, template_class)

    _pending_registrations.clear()
