"""
REST API endpoint to create update or delete use cases
"""
import json
import logging

import requests
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

log = logging.getLogger("fme_utils")


def usecase_to_discomap(usecase, operation):
    """
    notify FME the relevant operation on the usecase
    """
    topicsVocabulary = getUtility(
        IVocabularyFactory, name="clms.types.TopicsVocabulary"
    )(usecase)

    use_case_uid = usecase.UID()
    use_case_title = usecase.title
    try:
        use_case_summary = usecase.text.output
    except Exception as e:
        log.info(e)
        use_case_summary = ""

    submitting_production_year = usecase.submittingProducionYear
    responsible_organisation = usecase.responsibleOrganization
    contact_person_name_ = usecase.contactName
    contact_person_email_ = usecase.contactEmail
    use_case_topics = ",".join(
        [topicsVocabulary.getTerm(item).title for item in usecase.topics]
    )
    spatial_coverage = ",".join(usecase.taxonomy_use_case_spatial_coverage)
    use_case_outcome = usecase.outcome
    used_products = []
    if usecase.products:
        used_products = [
            api.content.get(UID=item).Title()
            for item in usecase.products
            if api.content.get(UID=item)
        ]
    used_datasets = []
    if usecase.datasets:
        used_datasets = [
            api.content.get(UID=item).Title()
            for item in usecase.datasets
            if api.content.get(UID=item)
        ]

    clms_products_used = "/".join(used_products + used_datasets)

    fme_data = {
        "publishedParameters": [
            {"name": "Use_case_title", "value": use_case_title},
            {"name": "Use_case_summary", "value": use_case_summary},
            {
                "name": "Use_case_submitting_production_year",
                "value": submitting_production_year,
            },
            {
                "name": "Responsible_organisation",
                "value": responsible_organisation,
            },
            {
                "name": "Contact_person_name_",
                "value": contact_person_name_,
            },
            {
                "name": "Contact_person_email_",
                "value": contact_person_email_,
            },
            {"name": "Use_case_topics", "value": "".join(use_case_topics)},
            {"name": "User_case_outcome", "value": use_case_outcome},
            {"name": "Spatial_coverage", "value": spatial_coverage},
            {
                "name": "Copernicus_Land_Monitoring_Service_products_used",
                "value": clms_products_used,
            },
            {"name": "Use_Case_id", "value": use_case_uid},
            {"name": "Operation", "value": operation},
        ]
    }
    if usecase.image:
        fme_data["publishedParameters"].append(
            {
                "name": "Link_to_image",
                "value": "{url}/@@download/image".format(
                    url=usecase.absolute_url()
                ),
            },
        )

    fme_url = api.portal.get_registry_record("clms.types.usecase_fme.fme_url")
    fme_token = api.portal.get_registry_record("clms.types.usecase_fme.token")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "Authorization": "fmetoken token={0}".format(fme_token),
    }
    data = json.dumps(fme_data)
    resp = requests.post(fme_url, data, headers=headers)
    log.info(resp)
    log.info(data)
    if resp.ok:
        fme_task_id = resp.json().get("id", None)

    if not fme_task_id:
        return {
            "status": "error",
            "msg": "Wrong request to FME",
        }

    return {
        "status": "ok",
        "msg": "FME task created. Task id: {0}".format(fme_task_id),
    }
