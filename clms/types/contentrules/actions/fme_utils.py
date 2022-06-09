"""
REST API endpoint to create update or delete use cases
"""
import json
import logging

import requests
from plone import api

log = logging.getLogger("Plone")


def usecase_to_discomap(usecase, operation):
    """
    notify FME the relevant operation on the usecase
    """
    clms_products_used = usecase.clms_products_used
    use_case_uid = usecase.UID()
    use_case_title = usecase.title
    use_case_summary = usecase.description
    submitting_production_year = usecase.submittingProducionYear
    responsible_organisation = usecase.responsibleOrganization
    contact_person_name_ = usecase.contactName
    contact_person_email_ = usecase.contactEmail
    use_case_topics = usecase.topics
    spatial_coverage = usecase.geographicCoverage
    user_case_outcome = usecase.outcome
    # links_to_documents = usecase.documentLinks or []
    # links_to_videos = usecase.videoLinks or []
    # links_to_web_sites = usecase.websiteLinks or []
    # upload_use_case_documents = usecase.upload_use_case_documents or []
    # upload_use_case_images = usecase.upload_use_case_images or []
    # upload_use_case_videos = usecase.upload_use_case_videos or []

    log.info(spatial_coverage)
    fme_data = {
        "publishedParameters": [
            {"name": "Use_case_title", "value": use_case_title},
            {
                "name": "Copernicus_Land_Monitoring_Service_products_used",
                "value": clms_products_used,
            },
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
            {
                "name": "Spatial_coverage",
                "value": "".join(
                    str(x) + "," for x in spatial_coverage.split(",")
                ),
            },
            {"name": "User_case_outcome", "value": user_case_outcome},
            # {
            #     "name": "Links_to_documents",
            #     "value": "".join(links_to_documents),
            # },
            # {"name": "Links_to_videos", "value": "".join(links_to_videos)},
            # {
            #     "name": "Links_to_web_sites",
            #     "value": "".join(links_to_web_sites),
            # },
            # {
            #     "name": "Upload_use_case_documents",
            #     "value": upload_use_case_documents,
            # },
            # {
            #     "name": "Upload_use_case_images",
            #     "value": upload_use_case_images,
            # },
            # {
            #     "name": "Upload_use_case_videos",
            #     "value": upload_use_case_videos,
            # },
            {"name": "Use_Case_id", "value": use_case_uid},
            {"name": "Operation", "value": operation},
        ]
    }

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
