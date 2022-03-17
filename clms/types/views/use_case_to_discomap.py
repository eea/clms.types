"""
REST API endpoint to create update or delete use cases
"""
import json
import requests
from Products.Five.browser import BrowserView


class useCaseToDiscomap(BrowserView):
    """Start of the view containing the functionality"""
    def __call__(self):
        """main method"""
        operation = dict(self.request)["REQUEST_METHOD"]
        clms_products_used = self.context.clms_products_used
        use_case_uid = self.context.UID()
        use_case_title = self.context.title
        use_case_summary = self.context.summary
        submitting_production_year = self.context.submittingProducionYear
        responsible_organisation = self.context.responsibleOrganization
        contact_person_name_ = self.context.contactName
        contact_person_email_ = self.context.contactEmail
        use_case_topics = self.context.topics
        spatial_coverage = self.context.geographicCoverage
        latitude = self.context.latitude
        longitude = self.context.longitude
        region = self.context.region
        lat_reg = self.context.lat_reg
        lon_reg = self.context.lon_reg
        bbox = self.context.bbox
        user_case_outcome = self.context.outcome
        links_to_documents = self.context.documentLinks
        links_to_videos = self.context.videoLinks
        links_to_web_sites = self.context.websiteLinks
        upload_use_case_documents = self.context.upload_use_case_documents
        upload_use_case_images = self.context.upload_use_case_images
        upload_use_case_videos = self.context.upload_use_case_videos
        origin_name = self.context.origin_name

        if 90 < latitude < -90:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong latitude value",
            }
        if 180 < longitude < -180:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong longitude value",
            }

        if 90 < lat_reg < -90:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "msg": "Wrong region latitude value",
            }
        if 180 < lon_reg < -180:
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
                    "value": clms_products_used
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
        return None
