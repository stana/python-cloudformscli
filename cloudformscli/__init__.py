import time

from cloudformscli import base
from cloudformscli import connection
from cloudformscli import exception


class Client(object):
    def __init__(self, base_uri, username, password, verify_cert=False):
        self._conn = connection.Connection(
            base_uri, username, password, verify_cert)

    def get_auth_token(self):
        return self._conn.get('auth')

    def set_token_auth(self, auth_token):
        return self._conn.set_token_auth(auth_token)

    @property
    def vms(self):
        return VmManager(self._conn)

    @property
    def gen_obj_defs(self):
        return GenericObjectDefManager(self._conn)

    def gen_objects(self, gen_obj_def_name=None):
        return GenericObjectManager(self._conn, gen_obj_def_name=gen_obj_def_name)

    @property
    def service_requests(self):
        return ServiceRequestManager(self._conn)

    @property
    def automation_requests(self):
        return AutomationRequestManager(self._conn)

    @property
    def tasks(self):
        return TaskManager(self._conn)

    @property
    def catalogs(self):
        return CatalogManager(self._conn)

    @property
    def services(self):
        return ServiceManager(self._conn)

    @property
    def service_templates(self):
        return ServiceTemplateManager(self._conn)

    def catalog_service_templates(self, catalog_id):
        return ServiceTemplateManager(self._conn, catalog_id)


class VmManager(base.BaseManager):
    def __init__(self, conn):
        super(VmManager, self).__init__(conn, 'vms')

class TaskManager(base.BaseManager):
    def __init__(self, conn):
        super(VmManager, self).__init__(conn, 'tasks')

class ServiceManager(base.BaseManager):
    def __init__(self, conn):
        super(ServiceManager, self).__init__(conn, 'services')

class CatalogManager(base.BaseManager):
    def __init__(self, conn):
        super(CatalogManager, self).__init__(conn, 'service_catalogs')

class ServiceTemplateManager(base.BaseManager):
    def __init__(self, conn, catalog_id=None):
        if catalog_id:
            rel_path = "service_catalogs/%s/service_templates" % catalog_id
        else:
            rel_path = 'service_templates'
        super(ServiceTemplateManager, self).__init__(conn, rel_path)

class GenericObjectDefManager(base.BaseManager):
    def __init__(self, conn):
        super(GenericObjectDefManager, self).__init__(conn, 
            'generic_object_definitions')


class GenericObjectManager(base.BaseManager):
    """Manage generic objects of any definition type. Or use as
    base class for managing specific gen object definitions by
    passing in gen obj definition name.
    """
    def __init__(self, conn, gen_obj_def_name=None):
        self.gen_obj_def_name = gen_obj_def_name
        if gen_obj_def_name:
            base_params = {'filter[]': 'generic_object_definition_name=%s'
                % gen_obj_def_name}
        else:
            base_params = None
        super(GenericObjectManager, self).__init__(conn,
            'generic_objects', base_params=base_params)
        self.gen_obj_def = None
        if gen_obj_def_name:
            # This is a gen obj manager for a specific def type (eg. OvmVm).
            # Get gen obj definition - will need it in get_by_id
            # to make sure gen obj fetched is of correct type. For
            # example in OvmVmManager we only want to return OvmVm
            # type objects (not disk or nic gen objects).
            gen_obj_def_mngr = GenericObjectDefManager(conn)
            self.gen_obj_def = gen_obj_def_mngr.get_by_name(gen_obj_def_name)

    def get_by_id(self, id):
        # override here to also check if found resource is of correct
        # generic object definition (if gen obj def specified
        gen_obj = super(GenericObjectManager, self).get_by_id(id)
        if self.gen_obj_def:
            # Specific gen obj definition specified. Filter on it
            # as returned resource might not be of correct type.
            if gen_obj['generic_object_definition_id'] != self.gen_obj_def['id']:
                # gen obj found is not of correct type
                raise exception.ObjectNotFoundException(
                    "No generic object found with id - `%s` and `%s` type" %
                        (id, self.gen_obj_def_name))
        return gen_obj
