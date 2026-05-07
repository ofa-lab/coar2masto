from masto import get_config, get_client
from errors import Error

def handle_request(coar_request):
    conf_section = coar_request["origin"]["inbox"]

    config = get_config(section=conf_section) \
             or get_config(section="default.mastodon.api")

    m = get_client(config)
    msg = coar_to_masto(coar_request)
    m.status_post(msg)


def coar_to_masto(coar_request):
    return f"""
    to:   {coar_request["target"]["inbox"]}
    from: {coar_request["origin"]["inbox"]}
    type: {coar_request["type"]}

    {coar_request_as_text(coar_request)}
    """


def coar_request_as_text(coar_request):
    def endorsement():
        return f"""
        endorsement for: {coar_request['context']['ietf:cite-as']}
        recommendation:  {coar_request['object']['ietf:cite-as']}
        actor:  {coar_request['actor']['name']}
        """

    def review():
        return f"""
        review: {coar_request['object']['id']}
        actor:  {coar_request['actor']['name']}
        """

    req_type = coar_request.get("type")
    for typ, convert in {
        "Announce coar-notify:EndorsementAction": endorsement,
        "Announce coar-notify:ReviewAction": review,
    }.items():
        if all([t in req_type for t in typ.split()]):
            return convert()

    return f"no converter for type: {req_type}"


def validate_coar_request(post_request):
    if not post_request.content_type == "application/ld+json":
        raise Error(415, message="Content-type must be: application/ld+json")

    coar_request = post_request.get_json()
    context = coar_request.get("@context")

    if not context:
        raise Error(400, message="@context not found in request")
    if not "https://coar-notify.net" in context:
        raise Error(400, message="@context must contain 'https://coar-notify.net'")
    req_type = coar_request.get("type")
    if not req_type:
        raise Error(400, message="type not found in request")
    req_target = coar_request.get("target")
    if not req_target:
        raise Error(400, message="target not found in request")
    req_origin = coar_request.get("origin")
    if not req_origin:
        raise Error(400, message="origin not found in request")
    if req_target.get("inbox") is None:
        raise Error(400, message="target.inbox not found")
    if not req_origin.get("inbox"):
        raise Error(400, message="origin.inbox not found")

    return coar_request
