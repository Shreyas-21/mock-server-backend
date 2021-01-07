from django.db import transaction
from django.views.decorators.http import require_GET, require_POST

from .validators import *
from .selectors import base_endpoints_get, relative_endpoints_get, schemas_get
from .services import base_endpoint_add, relative_endpoint_add, schema_add, endpoint_schema_update, \
	relative_endpoint_update, relative_endpoint_delete, data_export, data_import


@require_GET
def check_server_status(_):
	return dict()


@require_GET
def get_base_endpoints(_):
	return dict(baseEndpoints=base_endpoints_get())


@require_POST
@create_base_endpoint_schema
def add_base_endpoint(request):
	data = request.json
	endpoint = base_endpoint_add(data)
	return dict(id=endpoint.id)


@require_GET
def get_relative_endpoints(_, base_endpoint_id):
	return dict(relativeEndpoints=relative_endpoints_get(base_endpoint_id))


@require_POST
@create_relative_endpoint_schema
def add_relative_endpoint(request):
	data = request.json
	relative_endpoint = relative_endpoint_add(data)
	return dict(
		id=relative_endpoint.id, regex_endpoint=relative_endpoint.regex_endpoint,
		url_params=relative_endpoint.url_params
	)


@require_POST
@update_endpoint_schema_schema
def update_endpoint_schema(request):
	data = request.json
	endpoint = endpoint_schema_update(data)
	return dict(fields=endpoint.fields.all().detail())


@require_GET
def get_schemas(_):
	return dict(schemas=schemas_get())


@require_POST
@create_schema_schema
@transaction.atomic
def add_schema(request):
	data = request.json
	schema = schema_add(data)
	return dict(schema=schema)


@require_POST
@create_relative_endpoint_schema
def update_relative_endpoint(request):
	data = request.json
	relative_endpoint_update(data)
	return dict()


@require_POST
@delete_endpoint_schema
def delete_relative_endpoint(request):
	data = request.json
	relative_endpoint_delete(data)
	return dict()


@require_GET
def export_data(request):
	data = data_export()
	return data


@require_POST
def import_data(request):
	data = request.json
	data_import(data)
	return dict()
