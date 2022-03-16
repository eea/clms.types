# -*- coding: utf-8 -*-

from ast import operator
from pydoc_data.topics import topics
from Products.Five.browser import BrowserView
import requests
from logging import getLogger
import json

log = getLogger(__name__)


class useCaseToDiscomap(BrowserView):

    def __call__(self):
        context = self.context
        operation = dict(self.request)["REQUEST_METHOD"]
        clms_products = context.Copernicus_Land_Monitoring_Service_products_used
        use_case_uid = context.UID()
        use_case_title = context.title
        use_case_summary = context.summary
        submitting_production_year = context.submittingProducionYear
        responsible_organisation = context.responsibleOrganization
        contact_person_name_ = context.contactName
        contact_person_email_ = context.contactEmail
        use_case_topics = context.topics
        spatial_coverage = context.geographicCoverage
        latitude = context.latitude
        longitude = context.longitude
        region = context.region
        lat_reg = context.lat_reg
        lon_reg = context.lon_reg
        bbox = context.bbox
        user_case_outcome = context.outcome
        links_to_documents = context.documentLinks
        links_to_videos = context.videoLinks
        links_to_web_sites = context.websiteLinks
        upload_use_case_documents = context.upload_use_case_documents
        upload_use_case_images = context.upload_use_case_images
        upload_use_case_videos = context.upload_use_case_videos
        origin_name = context.origin_name

        if latitude > 90 and latitude < -90:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong latitude value",
            }
        if longitude > 180 and longitude < -180:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong longitude value",
            }

        if lat_reg > 90 and lat_reg < -90:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong region latitude value",
            }
        if lon_reg > 180 and lon_reg < -180:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong region longitude value",
            }

        log.info(operation)
        if operation == "POST":
            operation = "INSERT"
        elif operation == "DELETE":
            operation = "DELETE"
        else:
            operation = "UPDATE"

        fme_data = {
            "publishedParameters": [{
                    "name": "Use_case_title",
                    "value": use_case_title
                }, {
                    "name": "Copernicus_Land_Monitoring_Service_products_used",
                    "value": clms_products
                }, {
                    "name": "Use_case_summary",
                    "value": use_case_summary
                }, {
                    "name": "Use_case_submitting_production_year",
                    "value": submitting_production_year
                }, {
                    "name": "Responsible_organisation",
                    "value": responsible_organisation
                }, {
                    "name": "Contact_person_name_",
                    "value": contact_person_name_
                }, {
                    "name": "Contact_person_email_",
                    "value": contact_person_email_
                }, {
                    "name": "Use_case_topics",
                    "value": "".join(use_case_topics)
                }, {
                    "name": "Spatial_coverage",
                    "value": "".join(spatial_coverage)
                }, {
                    "name": "Latitude",
                    "value": latitude
                }, {
                    "name": "Longitude",
                    "value": longitude
                }, {
                    "name": "Region",
                    "value": region
                }, {
                    "name": "lat_reg",
                    "value": lat_reg
                }, {
                    "name": "lon_reg",
                    "value": lon_reg
                }, {
                    "name": "BBOX",
                    "value": bbox
                }, {
                    "name": "User_case_outcome",
                    "value": user_case_outcome
                }, {
                    "name": "Links_to_documents",
                    "value": "".join(links_to_documents)
                }, {
                    "name": "Links_to_videos",
                    "value": "".join(links_to_videos)
                }, {
                    "name": "Links_to_web_sites",
                    "value": "".join(links_to_web_sites)
                }, {
                    "name": "Upload_use_case_documents",
                    "value": upload_use_case_documents
                }, {
                    "name": "Upload_use_case_images",
                    "value": upload_use_case_images
                }, {
                    "name": "Upload_use_case_videos",
                    "value": upload_use_case_videos
                }, {
                    "name": "Origin_name",
                    "value": origin_name
                }, {
                    "name": "Use_Case_id",
                    "value": use_case_uid
                }, {
                    "name": "Operation",
                    "value": operation
                }
            ]
        }

        FME_TOKEN = "2d6aaef2df4ba3667c883884f57a8b6bab2efc5e"
        FME_URL_PATH = "/v3/transformations/submit/CLMS/CLMS_UseCases.fmw"
        FME_URL = "https://copernicus-fme.eea.europa.eu/fmerest" + FME_URL_PATH
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Authorization": "fmetoken token={0}".format(FME_TOKEN),
        }
        data = json.dumps(fme_data)
        resp = requests.post(FME_URL, data, headers=headers)
        if resp.ok:
            fme_task_id = resp.json().get("id", None)

        if not fme_task_id:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong request to FME",
            }
