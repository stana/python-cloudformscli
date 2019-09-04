from cloudformscli import exception

class BaseManager(object):
    def __init__(self, conn, rel_url, base_params=None):
        self._conn = conn
        self._rel_url = rel_url
        self._base_params = base_params or {}

    def _get_expand_filter(self, resources_to_expand=None):
        # Details to expand when fetching resources. Depending on api endpoint 
        # resource_to_expand could have a string like -
        #   'resources', 'resources,tags', 'resources&attributes=flavor,hardware'
        # Default to 'resources'.
        return {'expand': resources_to_expand or 'resources'}

    def _get_all_params(self, params):
        # merge query string params base params (if any)
        all_params = self._base_params.copy()
        if params:
            all_params.update(params)
        return all_params 

    def get_all(self, expand=False, resources_to_expand=None):
        params = None
        if expand or resources_to_expand:
            params = self._get_expand_filter(resources_to_expand=resources_to_expand)
        return self._conn.get(self._rel_url, params=self._get_all_params(params))

    def _get_id_url(self, id):
        return '%s/%s' % (self._rel_url, id)

    def get_by_id(self, id):
        id_url = self._get_id_url(id)
        try:
            resource = self._conn.get(id_url)
            if hasattr(self, 'gen_obj_def'):
                # resource is a gen obj, filter on type
                if resource['generic_object_definition_id'] != self.gen_obj_def['id']:
                    # gen obj found is not of correct type
                    raise exception.ObjectNotFoundException(
                        "No resource found with id - %s and `OvmVm` type" % id)
            return resource
        except exception.CloudFormsClientRequestException as req_exc:
            if req_exc.http_status_code == 404:
                raise exception.ObjectNotFoundException(
                    "No resource found with id - %s" % id_url)
            raise req_exc

    def search_by_name(self, name, expand=False):
        query_filter = {'filter[]':  'name=%s' % name}
        if expand:
            query_filter.update(self._get_expand_filter())
        return self._conn.get(self._rel_url, params=self._get_all_params(query_filter))

    def get_by_name(self, name):
        res = self.search_by_name(name, expand=True)
        if not (res and res['resources']):
            raise exception.ObjectNotFoundException(
                "No resource found with name - %s" % name)
        if len(res['resources']) > 1:
            raise exception.TooManyObjectsException(
                "More than one resource found with name - %s" % name)
        return res['resources'][0]

    def get_id_by_name(self, name):
        resource = self.get_by_name(name)
        return resource['id']

    def action(self, id, action_name, data={}, params={}):
        rel_url = "%s/%s" % (self._get_id_url(id), action_name)
        data.update({'action': action_name})
        return self._conn.post(rel_url, data, params)

    #def delete(self, id):
    #    return self._conn.delete(self._get_id_url(id))
