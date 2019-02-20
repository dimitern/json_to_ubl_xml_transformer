from collections import OrderedDict

DEFAULT_ENCODING = "utf-8"
FALLBACK_ENCODING = "utf-8-sig"

# Constants used in naming and formatting of intermediate JSON.
LIST_ITEM = "{}__{}".format
ATTRIBUTE_PREFIX = "_"
VALUE_ATTRIBUTE = "__text"

# Names of special intermediate JSON elements.
ATTRIBUTES = "@attrs"
VALUE = "@value"
NAME = "@name"

# UBL Billing 3 Invoice intermediate JSON constants.
BILLING_NAMESPACE = (
    "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
)
PROFILE_NAMESPACE = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
INVOICE_NAMESPACE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
CAC_NAMESPACE = (
    "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
)
CBC_NAMESPACE = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

NAMESPACE = "{}:{{}}".format
CBC = NAMESPACE("cbc").format
CAC = NAMESPACE("cac").format

XML_NS = "xmlns"
XMLNS = "{}:{{}}".format(XML_NS).format

UBL_INVOICE_ROOT = OrderedDict(
    [
        (
            "Invoice",
            OrderedDict(
                [
                    (
                        ATTRIBUTES,
                        OrderedDict(
                            [
                                (XMLNS("cac"), CAC_NAMESPACE),
                                (XMLNS("cbc"), CBC_NAMESPACE),
                                (XML_NS, INVOICE_NAMESPACE),
                            ]
                        ),
                    ),
                    (CBC("CustomizationID"), BILLING_NAMESPACE),
                    (CBC("ProfileID"), PROFILE_NAMESPACE),
                ]
            ),
        )
    ]
)

CBC_ELEMENTS = (
    "AccountingCost",
    "ActualDeliveryDate",
    "AdditionalStreetName",
    "AllowanceChargeReason",
    "AllowanceChargeReasonCode",
    "AllowanceTotalAmount",
    "Amount",
    "BaseAmount",
    "BaseQuantity",
    "BuyerReference",
    "ChargeIndicator",
    "ChargeTotalAmount",
    "CityName",
    "CompanyID",
    "CompanyLegalForm",
    "CountrySubentity",
    "CustomizationID",
    "Description",
    "DocumentCurrencyCode",
    "DocumentDescription",
    "DocumentType",
    "DocumentTypeCode",
    "DueDate",
    "ElectronicMail",
    "EmbeddedDocumentBinaryObject",
    "EndDate",
    "EndpointID",
    "HolderName",
    "ID",
    "IdentificationCode",
    "InvoicedQuantity",
    "InvoiceTypeCode",
    "IssueDate",
    "Line",
    "LineExtensionAmount",
    "LineID",
    "MultiplierFactorNumeric",
    "Name",
    "NetworkID",
    "Note",
    "PayableAmount",
    "PayableRoundingAmount",
    "PaymentID",
    "PaymentMeansCode",
    "Percent",
    "PostalZone",
    "PrepaidAmount",
    "PriceAmount",
    "PrimaryAccountNumberID",
    "ProfileID",
    "RegistrationName",
    "SalesOrderID",
    "StartDate",
    "StreetName",
    "TaxableAmount",
    "TaxAmount",
    "TaxCurrencyCode",
    "TaxExclusiveAmount",
    "TaxExemptionReason",
    "TaxExemptionReasonCode",
    "TaxInclusiveAmount",
    "TaxPointDate",
    "Telephone",
    "URI",
    "Value",
)
