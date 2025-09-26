"""FHIR R5 Library Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Library(FHIRResourceBase):
    """FHIR R5 Library resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Library-specific fields."""
        self.url = None
        self.identifier = []
        self.version = None
        self.version_algorithm_string = None
        self.version_algorithm_coding = None
        self.name = None
        self.title = None
        self.subtitle = None
        self.status = None  # Required: draft | active | retired | unknown
        self.experimental = None
        self.type = None  # Required
        self.subject_codeable_concept = []
        self.subject_reference = []
        self.date = None
        self.publisher = None
        self.contact = []
        self.description = None
        self.use_context = []
        self.jurisdiction = []
        self.purpose = None
        self.usage = None
        self.copyright = None
        self.copyright_label = None
        self.approval_date = None
        self.last_review_date = None
        self.effective_period = None
        self.topic = []
        self.author = []
        self.editor = []
        self.reviewer = []
        self.endorser = []
        self.related_artifact = []
        self.parameter = []
        self.data_requirement = []
        self.content = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_library"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_library"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_library"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Library-specific fields to dictionary."""
        if self.url:
            result["url"] = self.url
        if self.identifier:
            result["identifier"] = self.identifier
        if self.version:
            result["version"] = self.version
        if self.version_algorithm_string:
            result["versionAlgorithmString"] = self.version_algorithm_string
        if self.version_algorithm_coding:
            result["versionAlgorithmCoding"] = self.version_algorithm_coding
        if self.name:
            result["name"] = self.name
        if self.title:
            result["title"] = self.title
        if self.subtitle:
            result["subtitle"] = self.subtitle
        if self.status:
            result["status"] = self.status
        if self.experimental is not None:
            result["experimental"] = self.experimental
        if self.type:
            result["type"] = self.type
        if self.subject_codeable_concept:
            result["subjectCodeableConcept"] = self.subject_codeable_concept
        if self.subject_reference:
            result["subjectReference"] = self.subject_reference
        if self.date:
            result["date"] = self.date
        if self.publisher:
            result["publisher"] = self.publisher
        if self.contact:
            result["contact"] = self.contact
        if self.description:
            result["description"] = self.description
        if self.use_context:
            result["useContext"] = self.use_context
        if self.jurisdiction:
            result["jurisdiction"] = self.jurisdiction
        if self.purpose:
            result["purpose"] = self.purpose
        if self.usage:
            result["usage"] = self.usage
        if self.copyright:
            result["copyright"] = self.copyright
        if self.copyright_label:
            result["copyrightLabel"] = self.copyright_label
        if self.approval_date:
            result["approvalDate"] = self.approval_date
        if self.last_review_date:
            result["lastReviewDate"] = self.last_review_date
        if self.effective_period:
            result["effectivePeriod"] = self.effective_period
        if self.topic:
            result["topic"] = self.topic
        if self.author:
            result["author"] = self.author
        if self.editor:
            result["editor"] = self.editor
        if self.reviewer:
            result["reviewer"] = self.reviewer
        if self.endorser:
            result["endorser"] = self.endorser
        if self.related_artifact:
            result["relatedArtifact"] = self.related_artifact
        if self.parameter:
            result["parameter"] = self.parameter
        if self.data_requirement:
            result["dataRequirement"] = self.data_requirement
        if self.content:
            result["content"] = self.content
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Library-specific fields from dictionary."""
        self.url = data.get("url")
        self.identifier = data.get("identifier", [])
        self.version = data.get("version")
        self.version_algorithm_string = data.get("versionAlgorithmString")
        self.version_algorithm_coding = data.get("versionAlgorithmCoding")
        self.name = data.get("name")
        self.title = data.get("title")
        self.subtitle = data.get("subtitle")
        self.status = data.get("status")
        self.experimental = data.get("experimental")
        self.type = data.get("type")
        self.subject_codeable_concept = data.get("subjectCodeableConcept", [])
        self.subject_reference = data.get("subjectReference", [])
        self.date = data.get("date")
        self.publisher = data.get("publisher")
        self.contact = data.get("contact", [])
        self.description = data.get("description")
        self.use_context = data.get("useContext", [])
        self.jurisdiction = data.get("jurisdiction", [])
        self.purpose = data.get("purpose")
        self.usage = data.get("usage")
        self.copyright = data.get("copyright")
        self.copyright_label = data.get("copyrightLabel")
        self.approval_date = data.get("approvalDate")
        self.last_review_date = data.get("lastReviewDate")
        self.effective_period = data.get("effectivePeriod")
        self.topic = data.get("topic", [])
        self.author = data.get("author", [])
        self.editor = data.get("editor", [])
        self.reviewer = data.get("reviewer", [])
        self.endorser = data.get("endorser", [])
        self.related_artifact = data.get("relatedArtifact", [])
        self.parameter = data.get("parameter", [])
        self.data_requirement = data.get("dataRequirement", [])
        self.content = data.get("content", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Library-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = ["draft", "active", "retired", "unknown"]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Type is required
        if not self.type:
            return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if library is active."""
        return self.status == "active"
    
    def get_library_type(self) -> Optional[str]:
        """Get library type code."""
        if isinstance(self.type, dict) and self.type.get("coding"):
            for coding in self.type["coding"]:
                if coding.get("code"):
                    return coding["code"]
        return None