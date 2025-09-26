#ifndef FHIR_FINANCIAL_H
#define FHIR_FINANCIAL_H

#include "fhir_datatypes.h"
#include "fhir_foundation.h"
#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Financial Resource Types - Support, General, and Claims

// Account Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // active | inactive | entered-in-error | on-hold | unknown
    FHIRCodeableConcept* billing_status;
    FHIRCodeableConcept* type;
    FHIRString* name;
    FHIRReference** subject;
    size_t subject_count;
    FHIRPeriod* service_period;
    struct AccountCoverage** coverage;
    size_t coverage_count;
    FHIRReference* owner;
    FHIRString* description;
    struct AccountGuarantor** guarantor;
    size_t guarantor_count;
    struct AccountDiagnosis** diagnosis;
    size_t diagnosis_count;
    struct AccountProcedure** procedure;
    size_t procedure_count;
    struct AccountRelatedAccount** related_account;
    size_t related_account_count;
    FHIRCodeableConcept* currency;
    struct AccountBalance** balance;
    size_t balance_count;
    FHIRPeriod* calculated_at;
} FHIRAccount;

// Account Coverage structure
typedef struct AccountCoverage {
    FHIRElement base;
    FHIRReference* coverage;
    FHIRPositiveInt* priority;
} AccountCoverage;

// Account Guarantor structure
typedef struct AccountGuarantor {
    FHIRElement base;
    FHIRReference* party;
    FHIRBoolean* on_hold;
    FHIRPeriod* period;
} AccountGuarantor;

// Account Diagnosis structure
typedef struct AccountDiagnosis {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRReference* condition;
    FHIRDateTime* date_of_diagnosis;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRBoolean* on_admission;
    FHIRCodeableConcept* package_code;
} AccountDiagnosis;

// Account Procedure structure
typedef struct AccountProcedure {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRReference* code;
    FHIRDateTime* date_of_service;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRCodeableConcept* package_code;
    FHIRReference** device;
    size_t device_count;
} AccountProcedure;

// Account Related Account structure
typedef struct AccountRelatedAccount {
    FHIRElement base;
    FHIRCodeableConcept* relationship;
    FHIRReference* account;
} AccountRelatedAccount;

// Account Balance structure
typedef struct AccountBalance {
    FHIRElement base;
    FHIRCodeableConcept* aggregate;
    FHIRCodeableConcept* term;
    FHIRBoolean* estimate;
    FHIRMoney* amount;
} AccountBalance;

// Coverage Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // active | cancelled | draft | entered-in-error
    FHIRCodeableConcept* kind;
    FHIRReference* policy_holder;
    FHIRReference* subscriber;
    FHIRString* subscriber_id;
    FHIRReference* beneficiary;
    FHIRString* dependent;
    FHIRCodeableConcept* relationship;
    FHIRPeriod* period;
    FHIRReference** insurer;
    size_t insurer_count;
    struct CoverageClass** class;
    size_t class_count;
    FHIRPositiveInt* order;
    FHIRString* network;
    struct CoverageCostToBeneficiary** cost_to_beneficiary;
    size_t cost_to_beneficiary_count;
    FHIRBoolean* subrogation;
    FHIRReference** contract;
    size_t contract_count;
    struct CoveragePaymentBy** payment_by;
    size_t payment_by_count;
} FHIRCoverage;

// Coverage Class structure
typedef struct CoverageClass {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRString* value;
    FHIRString* name;
} CoverageClass;

// Coverage Cost To Beneficiary structure
typedef struct CoverageCostToBeneficiary {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept* category;
    FHIRString* network;
    FHIRString* unit;
    FHIRString* term;
    FHIRQuantity* value_quantity;
    FHIRMoney* value_money;
    struct CoverageCostToBeneficiaryException** exception;
    size_t exception_count;
} CoverageCostToBeneficiary;

// Coverage Cost To Beneficiary Exception structure
typedef struct CoverageCostToBeneficiaryException {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRPeriod* period;
} CoverageCostToBeneficiaryException;

// Coverage Payment By structure
typedef struct CoveragePaymentBy {
    FHIRElement base;
    FHIRReference* party;
    FHIRString* responsibility;
} CoveragePaymentBy;

// Claim Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // active | cancelled | draft | entered-in-error
    FHIRCodeableConcept* type;
    FHIRCodeableConcept* sub_type;
    FHIRCode* use;  // claim | preauthorization | predetermination
    FHIRReference* patient;
    FHIRPeriod* billable_period;
    FHIRDateTime* created;
    FHIRReference* enterer;
    FHIRReference* insurer;
    FHIRReference* provider;
    FHIRCodeableConcept* priority;
    FHIRCodeableConcept* funds_reserve;
    struct ClaimRelated** related;
    size_t related_count;
    FHIRReference* prescription;
    FHIRReference* original_prescription;
    struct ClaimPayee* payee;
    FHIRReference* referral;
    struct ClaimEvent** event;
    size_t event_count;
    FHIRReference* encounter;
    struct ClaimCareTeam** care_team;
    size_t care_team_count;
    struct ClaimSupportingInfo** supporting_info;
    size_t supporting_info_count;
    struct ClaimDiagnosis** diagnosis;
    size_t diagnosis_count;
    struct ClaimProcedure** procedure;
    size_t procedure_count;
    struct ClaimInsurance** insurance;
    size_t insurance_count;
    struct ClaimAccident* accident;
    FHIRReference** employment_impacted;
    size_t employment_impacted_count;
    FHIRReference** hospitalization;
    size_t hospitalization_count;
    struct ClaimItem** item;
    size_t item_count;
    FHIRMoney* total;
} FHIRClaim;

// Claim Related structure
typedef struct ClaimRelated {
    FHIRElement base;
    FHIRReference* claim;
    FHIRCodeableConcept* relationship;
    FHIRString* reference;
} ClaimRelated;

// Claim Payee structure
typedef struct ClaimPayee {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRReference* party;
} ClaimPayee;

// Claim Event structure
typedef struct ClaimEvent {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRDateTime* when_date_time;
    FHIRPeriod* when_period;
} ClaimEvent;

// Claim Care Team structure
typedef struct ClaimCareTeam {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRReference* provider;
    FHIRBoolean* responsible;
    FHIRCodeableConcept* role;
    FHIRCodeableConcept* specialty;
} ClaimCareTeam;

// Claim Supporting Info structure
typedef struct ClaimSupportingInfo {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRCodeableConcept* category;
    FHIRCodeableConcept* code;
    FHIRDate* timing_date;
    FHIRPeriod* timing_period;
    FHIRBoolean* value_boolean;
    FHIRString* value_string;
    FHIRQuantity* value_quantity;
    FHIRAttachment* value_attachment;
    FHIRReference* value_reference;
    FHIRCodeableConcept* reason;
} ClaimSupportingInfo;

// Claim Diagnosis structure
typedef struct ClaimDiagnosis {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRCodeableConcept* diagnosis_codeable_concept;
    FHIRReference* diagnosis_reference;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRBoolean* on_admission;
    FHIRCodeableConcept* package_code;
} ClaimDiagnosis;

// Claim Procedure structure
typedef struct ClaimProcedure {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRDateTime* date;
    FHIRCodeableConcept* procedure_codeable_concept;
    FHIRReference* procedure_reference;
    FHIRReference** udi;
    size_t udi_count;
} ClaimProcedure;

// Claim Insurance structure
typedef struct ClaimInsurance {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRBoolean* focal;
    FHIRIdentifier* identifier;
    FHIRReference* coverage;
    FHIRString* business_arrangement;
    FHIRString** pre_auth_ref;
    size_t pre_auth_ref_count;
    FHIRReference* claims_response;
} ClaimInsurance;

// Claim Accident structure
typedef struct ClaimAccident {
    FHIRElement base;
    FHIRDate* date;
    FHIRCodeableConcept* type;
    FHIRAddress* location_address;
    FHIRReference* location_reference;
} ClaimAccident;

// Claim Item structure
typedef struct ClaimItem {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRPositiveInt** care_team_sequence;
    size_t care_team_sequence_count;
    FHIRPositiveInt** diagnosis_sequence;
    size_t diagnosis_sequence_count;
    FHIRPositiveInt** procedure_sequence;
    size_t procedure_sequence_count;
    FHIRPositiveInt** information_sequence;
    size_t information_sequence_count;
    FHIRCodeableConcept* revenue;
    FHIRCodeableConcept* category;
    FHIRCodeableConcept* product_or_service;
    FHIRCodeableConcept** product_or_service_end;
    size_t product_or_service_end_count;
    FHIRReference* request;
    FHIRCodeableConcept** modifier;
    size_t modifier_count;
    FHIRCodeableConcept** program_code;
    size_t program_code_count;
    FHIRDate* serviced_date;
    FHIRPeriod* serviced_period;
    FHIRCodeableConcept* location_codeable_concept;
    FHIRAddress* location_address;
    FHIRReference* location_reference;
    FHIRCodeableConcept* patient_paid;
    FHIRQuantity* quantity;
    FHIRMoney* unit_price;
    FHIRDecimal* factor;
    FHIRCodeableConcept* tax;
    FHIRMoney* net;
    FHIRReference** udi;
    size_t udi_count;
    FHIRCodeableConcept* body_site;
    struct ClaimItemDetail** detail;
    size_t detail_count;
} ClaimItem;

// Claim Item Detail structure
typedef struct ClaimItemDetail {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRCodeableConcept* trace_number;
    FHIRCodeableConcept* revenue;
    FHIRCodeableConcept* category;
    FHIRCodeableConcept* product_or_service;
    FHIRCodeableConcept** product_or_service_end;
    size_t product_or_service_end_count;
    FHIRCodeableConcept** modifier;
    size_t modifier_count;
    FHIRCodeableConcept** program_code;
    size_t program_code_count;
    FHIRCodeableConcept* patient_paid;
    FHIRQuantity* quantity;
    FHIRMoney* unit_price;
    FHIRDecimal* factor;
    FHIRCodeableConcept* tax;
    FHIRMoney* net;
    FHIRReference** udi;
    size_t udi_count;
    struct ClaimItemDetailSubDetail** sub_detail;
    size_t sub_detail_count;
} ClaimItemDetail;

// Claim Item Detail Sub Detail structure
typedef struct ClaimItemDetailSubDetail {
    FHIRElement base;
    FHIRPositiveInt* sequence;
    FHIRCodeableConcept* trace_number;
    FHIRCodeableConcept* revenue;
    FHIRCodeableConcept* category;
    FHIRCodeableConcept* product_or_service;
    FHIRCodeableConcept** product_or_service_end;
    size_t product_or_service_end_count;
    FHIRCodeableConcept** modifier;
    size_t modifier_count;
    FHIRCodeableConcept** program_code;
    size_t program_code_count;
    FHIRCodeableConcept* patient_paid;
    FHIRQuantity* quantity;
    FHIRMoney* unit_price;
    FHIRDecimal* factor;
    FHIRCodeableConcept* tax;
    FHIRMoney* net;
    FHIRReference** udi;
    size_t udi_count;
} ClaimItemDetailSubDetail;

// Function declarations for Financial resources

// Account functions
FHIRAccount* fhir_account_create(const char* id);
void fhir_account_free(FHIRAccount* account);
FHIRAccount* fhir_parse_account(cJSON* json);
cJSON* fhir_account_to_json(const FHIRAccount* account);
bool fhir_validate_account(const FHIRAccount* account);

// Coverage functions
FHIRCoverage* fhir_coverage_create(const char* id);
void fhir_coverage_free(FHIRCoverage* coverage);
FHIRCoverage* fhir_parse_coverage(cJSON* json);
cJSON* fhir_coverage_to_json(const FHIRCoverage* coverage);
bool fhir_validate_coverage(const FHIRCoverage* coverage);

// Claim functions
FHIRClaim* fhir_claim_create(const char* id);
void fhir_claim_free(FHIRClaim* claim);
FHIRClaim* fhir_parse_claim(cJSON* json);
cJSON* fhir_claim_to_json(const FHIRClaim* claim);
bool fhir_validate_claim(const FHIRClaim* claim);

// Utility functions for Financial resources
bool fhir_is_financial_resource(const char* resource_type);
bool fhir_is_active_account(const FHIRAccount* account);
bool fhir_is_active_coverage(const FHIRCoverage* coverage);
char* fhir_get_claim_total_amount(const FHIRClaim* claim);

#endif // FHIR_FINANCIAL_H