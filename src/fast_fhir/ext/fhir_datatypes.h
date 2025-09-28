#ifndef FHIR_DATATYPES_H
#define FHIR_DATATYPES_H

#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Forward declarations
struct FHIRElement;
struct FHIRExtension;

// Base FHIR Element structure
typedef struct FHIRElement {
    char* id;
    struct FHIRExtension** extensions;
    size_t extension_count;
} FHIRElement;

// Extension structure
typedef struct FHIRExtension {
    char* url;
    void* value;  // Can be any FHIR datatype
    char* value_type;
} FHIRExtension;

// Primitive Data Types
typedef struct {
    FHIRElement base;
    bool value;
} FHIRBoolean;

typedef struct {
    FHIRElement base;
    int value;
} FHIRInteger;

typedef struct {
    FHIRElement base;
    long long value;
} FHIRInteger64;

typedef struct {
    FHIRElement base;
    double value;
} FHIRDecimal;

typedef struct {
    FHIRElement base;
    char* value;
} FHIRString;

typedef struct {
    FHIRElement base;
    char* value;  // URI format
} FHIRUri;

typedef struct {
    FHIRElement base;
    char* value;  // URL format
} FHIRUrl;

typedef struct {
    FHIRElement base;
    char* value;  // Canonical URL
} FHIRCanonical;

typedef struct {
    FHIRElement base;
    char* value;  // Base64 encoded
} FHIRBase64Binary;

typedef struct {
    FHIRElement base;
    char* value;  // Instant format (YYYY-MM-DDTHH:mm:ss.sss+zz:zz)
} FHIRInstant;

typedef struct {
    FHIRElement base;
    char* value;  // Date format (YYYY, YYYY-MM, or YYYY-MM-DD)
} FHIRDate;

typedef struct {
    FHIRElement base;
    char* value;  // DateTime format
} FHIRDateTime;

typedef struct {
    FHIRElement base;
    char* value;  // Time format (HH:mm:ss)
} FHIRTime;

typedef struct {
    FHIRElement base;
    char* value;  // Code format
} FHIRCode;

typedef struct {
    FHIRElement base;
    char* value;  // OID format
} FHIROid;

typedef struct {
    FHIRElement base;
    char* value;  // UUID format
} FHIRUuid;

typedef struct {
    FHIRElement base;
    char* value;  // Markdown text
} FHIRMarkdown;

typedef struct {
    FHIRElement base;
    unsigned int value;
} FHIRUnsignedInt;

typedef struct {
    FHIRElement base;
    unsigned int value;  // 1 or greater
} FHIRPositiveInt;

// General Purpose Data Types
typedef struct {
    FHIRElement base;
    char* system;
    char* version;
    char* code;
    char* display;
    bool user_selected;
} FHIRCoding;

typedef struct {
    FHIRElement base;
    FHIRCoding** coding;
    size_t coding_count;
    char* text;
} FHIRCodeableConcept;

typedef struct {
    FHIRElement base;
    double value;
    char* comparator;  // <, <=, >=, >, ad
    char* unit;
    char* system;
    char* code;
} FHIRQuantity;

typedef FHIRQuantity FHIRAge;
typedef FHIRQuantity FHIRCount;
typedef FHIRQuantity FHIRDistance;
typedef FHIRQuantity FHIRDuration;
typedef FHIRQuantity FHIRMoney;
typedef FHIRQuantity FHIRSimpleQuantity;

typedef struct {
    FHIRElement base;
    double low;
    double high;
} FHIRRange;

typedef struct {
    FHIRElement base;
    FHIRQuantity* numerator;
    FHIRQuantity* denominator;
} FHIRRatio;

typedef struct {
    FHIRElement base;
    FHIRRange* numerator;
    FHIRQuantity* denominator;
} FHIRRatioRange;

typedef struct {
    FHIRElement base;
    FHIRDate* start;
    FHIRDate* end;
} FHIRPeriod;

typedef struct {
    FHIRElement base;
    char* use;  // usual, official, temp, nickname, anonymous, old, maiden
    char* text;
    char** family;
    size_t family_count;
    char** given;
    size_t given_count;
    char** prefix;
    size_t prefix_count;
    char** suffix;
    size_t suffix_count;
    FHIRPeriod* period;
} FHIRHumanName;

typedef struct {
    FHIRElement base;
    char* use;  // home, work, temp, old, mobile
    char* system;  // phone, fax, email, pager, url, sms, other
    char* value;
    unsigned int rank;
    FHIRPeriod* period;
} FHIRContactPoint;

typedef struct {
    FHIRElement base;
    char* use;  // home, work, temp, old, billing
    char* type;  // postal, physical, both
    char* text;
    char** line;
    size_t line_count;
    char* city;
    char* district;
    char* state;
    char* postal_code;
    char* country;
    FHIRPeriod* period;
} FHIRAddress;

typedef struct {
    FHIRElement base;
    char* use;  // usual, official, secondary, old
    char* type;
    char* system;
    char* value;
    FHIRPeriod* period;
    void* assigner;  // Reference to Organization
} FHIRIdentifier;

typedef struct {
    FHIRElement base;
    char* reference;
    char* type;
    FHIRIdentifier* identifier;
    char* display;
} FHIRReference;

typedef struct {
    FHIRElement base;
    char* content_type;
    char* language;
    char* data;  // Base64 encoded
    char* url;
    unsigned int size;
    char* hash;  // SHA-1 hash
    char* title;
    FHIRInstant* creation;
    FHIRPeriod* height;
    FHIRPeriod* width;
    FHIRPositiveInt* frames;
    FHIRDecimal* duration;
    FHIRPositiveInt* pages;
} FHIRAttachment;

// Metadata Data Types
typedef struct {
    FHIRElement base;
    char* name;
    char* value;
} FHIRContactDetail;

typedef struct {
    FHIRElement base;
    char* name;
    FHIRContactPoint** telecom;
    size_t telecom_count;
} FHIRContributor;

typedef struct {
    FHIRElement base;
    char* type;  // documentation, justification, citation, predecessor, successor, derived-from, depends-on, composed-of
    char* label;
    char* display;
    char* citation;
    char* url;
    FHIRAttachment* document;
    FHIRReference* resource;
} FHIRRelatedArtifact;

typedef struct {
    FHIRElement base;
    char* type;  // created, published, reviewed, endorsed, derived, unknown
    FHIRDate* date;
    FHIRContactDetail** author;
    size_t author_count;
    FHIRContactDetail** editor;
    size_t editor_count;
    FHIRContactDetail** reviewer;
    size_t reviewer_count;
    FHIRContactDetail** endorser;
    size_t endorser_count;
} FHIRDataRequirement;

typedef struct {
    FHIRElement base;
    char* description;
    char* type;  // create, update, remove, fireEvent
    char* label;
    char* title;
    char* prefix;
    char* priority;
    FHIRCodeableConcept* code;
    char* reason;
    char* documentation;
    char* goal_id;
    char* subject_codeable_concept;
    FHIRReference* subject_reference;
    char* trigger;
    char* condition;
    char* input;
    char* output;
    char* related_action;
    char* timing;
    char* participant;
    char* type_canonical;
    char* type_uri;
    char* definition_canonical;
    char* definition_uri;
    char* transform;
    char* dynamic_value;
} FHIRPlanDefinition;

// Special Purpose Data Types
typedef struct {
    FHIRElement base;
    char* div;  // XHTML content
} FHIRNarrative;

typedef struct {
    FHIRElement base;
    char* version_id;
    FHIRInstant* last_updated;
    FHIRUri* source;
    char** profile;
    size_t profile_count;
    FHIRCoding** security;
    size_t security_count;
    FHIRCoding** tag;
    size_t tag_count;
} FHIRMeta;

typedef struct {
    FHIRElement base;
    char* path;
    char* representation;  // xmlAttr, xmlText, typeAttr, cdaText, xhtml
    char* slice_name;
    bool slice_is_constraining;
    char* label;
    FHIRCoding** code;
    size_t code_count;
    char* slicing;
    char* short_description;
    char* definition;
    char* comment;
    char* requirements;
    char** alias;
    size_t alias_count;
    unsigned int min;
    char* max;  // Can be number or "*"
    char* base_path;
    char* content_reference;
    char* type;
    char* default_value;
    char* meaning_when_missing;
    char* order_meaning;
    char* fixed_value;
    char* pattern_value;
    char* example;
    char* min_value;
    char* max_value;
    int max_length;
    char** condition;
    size_t condition_count;
    char* constraint;
    bool must_support;
    bool is_modifier;
    char* is_modifier_reason;
    bool is_summary;
    char* binding;
    char* mapping;
} FHIRElementDefinition;

typedef struct {
    FHIRElement base;
    char* type;  // Parameter, Let
    char* name;
    char* use;  // in, out
    int min;
    char* max;
    char* documentation;
    char* type_name;
    char* target_profile;
    char* search_type;
    char* binding;
    char* referenced_from;
    char* part;
} FHIRParameterDefinition;

typedef struct {
    FHIRElement base;
    char* type;  // create, update, delete, historyInstance, historyType, read, vread, search-type, search-system, capabilities
    char* resource;
    char* label;
    char* description;
    bool accept;
    char* content_type;
    char* destination;
    bool encode_request_url;
    char* method;  // delete, get, options, patch, post, put, head
    char* origin;
    char* params;
    char* request_header;
    char* request_id;
    char* response_id;
    char* source_id;
    char* target_id;
    char* url;
} FHIRTestScriptSetupActionOperation;

// Function declarations for creating and manipulating data types
FHIRElement* fhir_element_create(const char* id);
void fhir_element_free(FHIRElement* element);

FHIRString* fhir_string_create(const char* value);
FHIRBoolean* fhir_boolean_create(bool value);
FHIRInteger* fhir_integer_create(int value);
FHIRDecimal* fhir_decimal_create(double value);

FHIRCoding* fhir_coding_create(const char* system, const char* code, const char* display);
FHIRCodeableConcept* fhir_codeable_concept_create(const char* text);
FHIRQuantity* fhir_quantity_create(double value, const char* unit, const char* system, const char* code);
FHIRIdentifier* fhir_identifier_create(const char* system, const char* value);
FHIRReference* fhir_reference_create(const char* reference, const char* display);

// JSON parsing functions
FHIRElement* fhir_parse_element(cJSON* json);
FHIRString* fhir_parse_string(cJSON* json);
FHIRBoolean* fhir_parse_boolean(cJSON* json);
FHIRInteger* fhir_parse_integer(cJSON* json);
FHIRDecimal* fhir_parse_decimal(cJSON* json);
FHIRCoding* fhir_parse_coding(cJSON* json);
FHIRCodeableConcept* fhir_parse_codeable_concept(cJSON* json);
FHIRQuantity* fhir_parse_quantity(cJSON* json);
FHIRIdentifier* fhir_parse_identifier(cJSON* json);
FHIRReference* fhir_parse_reference(cJSON* json);
FHIRHumanName* fhir_parse_human_name(cJSON* json);
FHIRContactPoint* fhir_parse_contact_point(cJSON* json);
FHIRAddress* fhir_parse_address(cJSON* json);
FHIRPeriod* fhir_parse_period(cJSON* json);

// JSON serialization functions
cJSON* fhir_element_to_json(const FHIRElement* element);
cJSON* fhir_string_to_json(const FHIRString* str);
cJSON* fhir_boolean_to_json(const FHIRBoolean* boolean);
cJSON* fhir_integer_to_json(const FHIRInteger* integer);
cJSON* fhir_decimal_to_json(const FHIRDecimal* decimal);
cJSON* fhir_coding_to_json(const FHIRCoding* coding);
cJSON* fhir_codeable_concept_to_json(const FHIRCodeableConcept* concept);
cJSON* fhir_quantity_to_json(const FHIRQuantity* quantity);
cJSON* fhir_identifier_to_json(const FHIRIdentifier* identifier);
cJSON* fhir_reference_to_json(const FHIRReference* reference);
cJSON* fhir_human_name_to_json(const FHIRHumanName* name);
cJSON* fhir_contact_point_to_json(const FHIRContactPoint* contact);
cJSON* fhir_address_to_json(const FHIRAddress* address);
cJSON* fhir_period_to_json(const FHIRPeriod* period);

// Validation functions
bool fhir_validate_uri(const char* uri);
bool fhir_validate_url(const char* url);
bool fhir_validate_date(const char* date);
bool fhir_validate_datetime(const char* datetime);
bool fhir_validate_instant(const char* instant);
bool fhir_validate_time(const char* time);
bool fhir_validate_code(const char* code);
bool fhir_validate_oid(const char* oid);
bool fhir_validate_uuid(const char* uuid);

// Utility functions
char* fhir_string_duplicate(const char* str);
void fhir_string_free(char* str);
char** fhir_string_array_create(size_t size);
void fhir_string_array_free(char** array, size_t size);

// FHIR typed string utility functions
void fhir_uri_free(FHIRUri* uri);
void fhir_code_free(FHIRCode* code);
void fhir_markdown_free(FHIRMarkdown* markdown);
void fhir_datetime_free(FHIRDateTime* datetime);
void fhir_instant_free(FHIRInstant* instant);
void fhir_canonical_free(FHIRCanonical* canonical);
void fhir_base64binary_free(FHIRBase64Binary* binary);

#endif // FHIR_DATATYPES_H