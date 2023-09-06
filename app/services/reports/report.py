from app.services.base import CRUDBase
from app.models.reports.report import Report
from app.serializers.reports.report import ReportCreateRequest, ReportUpdateRequest
    
srv_report = CRUDBase[Report, ReportCreateRequest, ReportUpdateRequest]
