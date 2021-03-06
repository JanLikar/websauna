from websauna.system.admin.interfaces import IAdmin
from websauna.system.core.traversal import Resource
from websauna.system.model.meta import Base


def get_admin(request) -> IAdmin:
    """Get hold of the default site admin interface root object."""
    admin_class = request.registry.queryUtility(IAdmin)
    return admin_class(request)


def get_admin_for_model(admin:IAdmin, model:type) -> Resource:
    """Return Admin resource for a model manager interface."""

    model_manager = admin["models"]

    if not model.id in model_manager:
        raise KeyError("No admin defined for model: {}".format(model))
    return model_manager[model.id]


def get_model_admin_for_sqlalchemy_object(admin:IAdmin, instance:type) -> Resource:
    """Return Admin resource for a SQLAlchemy object instance.

    :param admin: Admin root object

    :param instance: SQLAlchemy object
    """

    model_manager = admin["models"]

    registry = admin.request.registry
    model = instance.__class__

    model_admin_id = registry.model_admin_ids_by_model.get(model)
    assert model_admin_id, "No ModelAdmin configured for model {}".format(model)

    return model_manager[model_admin_id]


def get_admin_url_for_sqlalchemy_object(admin: IAdmin, instance: object, view_name: str=None) -> str:
    """Return direct URL to the admin view page of this object:

    Example:

    .. code-block:: python

        link = get_admin_url_for_sqlalchemy_object(request.admin, choice, view_name="edit")

    :param admin: Admin root object

    :param instance: SQLAlchemy object
    """
    model_admin = get_model_admin_for_sqlalchemy_object(admin, instance)
    return model_admin.get_object_url(instance, view_name=view_name)

