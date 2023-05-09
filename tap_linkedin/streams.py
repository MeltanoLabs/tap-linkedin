"""Stream type classes for tap-linkedin-sdk."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import singer_sdk

from singer_sdk import typing as th  # JSON Schema typing helpers

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType


from tap_linkedin.client import LinkedInStream

import pendulum, requests

from datetime import datetime

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class accounts(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts#search-for-accounts
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    columns = [
        "CHANGE_AUDIT_STAMPS",
        "CREATED_TIME",
        "CURRENCY",
        "ID",
        "LAST_MODIFIED_TIME",
        "NAME",
        "NOTIFIED_ON_CAMPAIGN_OPTIMIZATION",
        "NOTIFIED_ON_CREATIVE_APPROVAL",
        "NOTIFIED_ON_CREATIVE_REJECTION",
        "NOTIFIED_ON_END_OF_CAMPAIGN",
        "NOTIFIED_ON_NEW_FEATURES_ENABLED",
        "REFERENCE",
        "REFERENCE_ORGANIZATION_ID",
        "REFERENCE_PERSON_ID",
        "SERVING_STATUSES",
        "STATUS",
        "TEST",
        "TOTAL_BUDGET",
        "TOTAL_BUDGET_ENDS_AT",
        "TYPE",
        "VERSION",
    ]

    name = "account"
    replication_keys = ["last_modified_time"]
    primary_keys = ["last_modified_time", "id"]
    replication_method = "incremental"
    path = "adAccounts"

    schema = PropertiesList(
        Property(
            "changeAuditStamps",
            ObjectType(
                Property(
                    "created",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
                Property(
                    "lastModified",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
            ),
        ),
        Property("created_time", StringType),
        Property("last_modified_time", StringType),
        Property("currency", StringType),
        Property("id", IntegerType),
        Property("name", StringType),
        Property("notifiedOnCampaignOptimization", BooleanType),
        Property("notifiedOnCreativeApproval", BooleanType),
        Property("notifiedOnCreativeRejection", BooleanType),
        Property("notifiedOnEndOfCampaign", BooleanType),
        Property("notifiedOnNewFeaturesEnabled", BooleanType),
        Property("reference", StringType),
        Property("reference_organization_id", IntegerType),
        Property("reference_person_id", StringType),
        Property("servingStatuses", th.ArrayType(Property("items", StringType))),
        Property("status", StringType),
        Property(
            "total_budget",
            ObjectType(
                Property("amount", StringType),
                Property("currency_code", StringType),
                additional_properties=False,
            ),
        ),
        Property("total_budget_ends_at", StringType),
        Property("type", StringType),
        Property("test", BooleanType),
        Property(
            "version",
            ObjectType(Property("versionTag", StringType), additional_properties=False),
        ),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["q"] = "search"
        params["sort.field"] = "ID"
        params["sort.order"] = "ASCENDING"

        return params



class adAnalyticsByCampaignInit(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting#analytics-finder
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    name = "AdAnalyticsByCampaignInit"
    replication_keys = ["dateRange"]
    replication_method = "incremental"
    primary_keys = ["campaign_id", "dateRange"]
    path = "adAnalytics"

    schema = PropertiesList(
        Property("campaign_id", IntegerType),
        Property("documentCompletions", IntegerType),
        Property("documentFirstQuartileCompletions", IntegerType),
        Property("clicks", IntegerType),
        Property("documentMidpointCompletions", IntegerType),
        Property("documentThirdQuartileCompletions", IntegerType),
        Property("downloadClicks", IntegerType),
        Property("jobApplications", StringType),
        Property("jobApplyClicks", StringType),
        Property("postViewJobApplications", StringType),
        Property("costInUsd", StringType),
        Property("postViewRegistrations", StringType),
        Property("registrations", StringType),
        Property("talentLeads", IntegerType),
        Property("viralDocumentCompletions", IntegerType),
        Property("viralDocumentFirstQuartileCompletions", IntegerType),
        Property("viralDocumentMidpointCompletions", IntegerType),
        Property("viralDocumentThirdQuartileCompletions", IntegerType),
        Property("viralDownloadClicks", IntegerType),
        Property("viralJobApplications", StringType),
        Property("viralJobApplyClicks", StringType),
        Property("costInLocalCurrency", StringType),
        Property("viralRegistrations", StringType),
        Property("approximateUniqueImpressions", IntegerType),
        Property("cardClicks", IntegerType),
        Property("cardImpressions", IntegerType),
        Property("commentLikes", IntegerType),
        Property("viralCardClicks", IntegerType),
        Property("viralCardImpressions", IntegerType),
        Property("viralCommentLikes", IntegerType),
        Property("actionClicks", IntegerType),
        Property("adUnitClicks", IntegerType),
        Property("comments", IntegerType),
        Property("companyPageClicks", IntegerType),
        Property("conversionValueInLocalCurrency", StringType),
        Property(
            "dateRange",
            ObjectType(
                Property(
                    "end",
                    ObjectType(
                        Property("day", IntegerType),
                        Property("month", IntegerType),
                        Property("year", IntegerType),
                        additional_properties=False,
                    ),
                ),
                Property(
                    "start",
                    ObjectType(
                        Property("day", IntegerType),
                        Property("month", IntegerType),
                        Property("year", IntegerType),
                        additional_properties=False,
                    ),
                ),
            ),
        ),

        Property("day", StringType),
        Property("externalWebsiteConversions", IntegerType),
        Property("externalWebsitePostClickConversions", IntegerType),
        Property("externalWebsitePostViewConversions", IntegerType),
        Property("follows", IntegerType),
        Property("fullScreenPlays", IntegerType),
        Property("impressions", IntegerType),
        Property("landingPageClicks", IntegerType),
        Property("leadGenerationMailContactInfoShares", IntegerType),
        Property("leadGenerationMailInterestedClicks", IntegerType),
        Property("likes", IntegerType),
        Property("oneClickLeadFormOpens", IntegerType),
        Property("oneClickLeads", IntegerType),
        Property("opens", IntegerType),
        Property("otherEngagements", IntegerType),
        Property("pivot", StringType),
        Property("pivotValue", StringType),
        Property("sends", IntegerType),
        Property("shares", IntegerType),
        Property("textUrlClicks", IntegerType),
        Property("totalEngagements", IntegerType),
        Property("videoCompletions", IntegerType),
        Property("videoFirstQuartileCompletions", IntegerType),
        Property("videoMidpointCompletions", IntegerType),
        Property("videoStarts", IntegerType),
        Property("videoThirdQuartileCompletions", IntegerType),
        Property("videoViews", IntegerType),
        Property("viralClicks", IntegerType),
        Property("viralComments", IntegerType),
        Property("viralCompanyPageClicks", IntegerType),
        Property("viralExternalWebsiteConversions", IntegerType),
        Property("viralExternalWebsitePostClickConversions", IntegerType),
        Property("viralExternalWebsitePostViewConversions", IntegerType),
        Property("viralFollows", IntegerType),
        Property("viralFullScreenPlays", IntegerType),
        Property("viralImpressions", IntegerType),
        Property("viralLandingPageClicks", IntegerType),
        Property("viralLikes", IntegerType),
        Property("viralOneClickLeadFormOpens", IntegerType),
        Property("viralOneclickLeads", IntegerType),
        Property("viralOtherEngagements", IntegerType),
        Property("viralReactions", IntegerType),
        Property("reactions", IntegerType),
        Property("viralShares", IntegerType),
        Property("viralTotalEngagements", IntegerType),
        Property("viralVideoCompletions", IntegerType),
        Property("viralVideoFirstQuartileCompletions", IntegerType),
        Property("viralVideoMidpointCompletions", IntegerType),
        Property("viralVideoStarts", IntegerType),
        Property("viralVideoThirdQuartileCompletions", IntegerType),
        Property("viralVideoViews", IntegerType),
    ).to_dict()

    @property
    def adanalyticscolumns(self):
        columns = [
            "viralLandingPageClicks,viralExternalWebsitePostClickConversions,externalWebsiteConversions,viralVideoFirstQuartileCompletions,leadGenerationMailContactInfoShares,clicks,viralClicks,shares,viralFullScreenPlays,videoMidpointCompletions,viralCardClicks,viralExternalWebsitePostViewConversions,viralTotalEngagements,viralCompanyPageClicks,actionClicks,viralShares,videoCompletions,comments,externalWebsitePostViewConversions,dateRange",
            "costInUsd,landingPageClicks,oneClickLeadFormOpens,talentLeads,sends,viralOneClickLeadFormOpens,conversionValueInLocalCurrency,viralFollows,otherEngagements,viralVideoCompletions,cardImpressions,leadGenerationMailInterestedClicks,opens,totalEngagements,videoViews,viralImpressions,viralVideoViews,commentLikes,pivot,viralLikes",
            "adUnitClicks,videoThirdQuartileCompletions,cardClicks,likes,viralComments,viralVideoMidpointCompletions,viralVideoThirdQuartileCompletions,oneClickLeads,fullScreenPlays,viralCardImpressions,follows,videoStarts,videoFirstQuartileCompletions,textUrlClicks,pivotValue,reactions,viralReactions,externalWebsitePostClickConversions,viralOtherEngagements,costInLocalCurrency",
            "viralVideoStarts,viralRegistrations,viralJobApplyClicks,viralJobApplications,jobApplications,jobApplyClicks,viralExternalWebsiteConversions,postViewRegistrations,companyPageClicks,documentCompletions,documentFirstQuartileCompletions,documentMidpointCompletions,documentThirdQuartileCompletions,downloadClicks,viralDocumentCompletions,viralDocumentFirstQuartileCompletions,viralDocumentMidpointCompletions,viralDocumentThirdQuartileCompletions,viralDownloadClicks,impressions",
        ]

        return columns

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CAMPAIGN"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year

        params["fields"] = columns[0]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        # This function extracts day, month, and year from date rannge column
        # These values are aprsed with datetime function and the date is added to the day column
        try:
            daterange_day = row.get("dateRange").get("start").get("day")
            daterange_month = row.get("dateRange").get("start").get("month")
            daterange_year = row.get("dateRange").get("start").get("year")
            daterange_column = "{}-{}-{}".format(
                daterange_year, daterange_month, daterange_day
            )
            row["day"] = datetime.strptime(daterange_column, "%Y-%m-%d")
        except:
            pass
        try:
            campaign_column = row.get("pivotValue")
            campaign_column = int(campaign_column.split(":")[3])
            row["campaign_id"] = campaign_column
        except:
            pass

        return super().post_process(row, context)


class adAnalyticsByCampaign(adAnalyticsByCampaignInit):
    name = "ad_analytics_by_campaign"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CAMPAIGN"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["fields"] = columns[1]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """Return a dictionary of records from adanalytics classes

        Args:
            context: The stream context.

        Returns:
            A dictionary of records given from adanalytics streams
            Adanalytics classes: adanalyticsinit_stream, adanalyticsecond_stream, adanalyticsthird_stream
            Adanalytics classes gives a dictionary of records with 20 columns
            super() calls the records of adAnalyticsByCampaign class
            These classes are generator objects so they can't be merged unless we convert them into lists
            list() converts generator objects into lists
            merge_dicts() merges these classes
        """
        adanalyticsinit_stream = adAnalyticsByCampaignInit(
            self._tap, schema={"properties": {}}
        )
        adanalyticsecond_stream = adAnalyticsByCampaignSecond(
            self._tap, schema={"properties": {}}
        )
        adanalyticsthird_stream = adAnalyticsByCampaignThird(
            self._tap, schema={"properties": {}}
        )
        adanalytics_records = [
            self.merge_dicts(x, y, z, p)
            for x, y, z, p in zip(
                list(adanalyticsinit_stream.get_records(context)),
                list(super().get_records(context)),
                list(adanalyticsecond_stream.get_records(context)),
                list(adanalyticsthird_stream.get_records(context)),
            )
        ]

        return adanalytics_records

    def merge_dicts(self, *dict_args):
        """
        Given any number of dictionaries, shallow copy and merge into a new dict,
        precedence goes to key-value pairs in latter dictionaries.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result


class adAnalyticsByCampaignSecond(adAnalyticsByCampaignInit):
    name = "adanalyticsbycampaign_second"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CAMPAIGN"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["fields"] = columns[2]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params


class adAnalyticsByCampaignThird(adAnalyticsByCampaignInit):
    name = "adanalyticsbycampaign_third"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CAMPAIGN"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["fields"] = columns[3]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params


class videoAds(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-video#finders
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    name = "video_ads"
    replication_keys = ["last_modified_time"]
    replication_method = "incremental"
    primary_keys = ["last_modified_time"]
    path = "adDirectSponsoredContents"

    schema = PropertiesList(
        Property("account", StringType),
        Property("account_id", IntegerType),
        Property(
            "changeAuditStamps",
            ObjectType(
                Property(
                    "created",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
                Property(
                    "lastModified",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
            ),
        ),
        Property("created_time", StringType),
        Property("last_modified_time", StringType),
        Property("content_reference", StringType),
        Property("content_reference_ucg_post_id", IntegerType),
        Property("content_reference_share_id", IntegerType),
        Property("name", StringType),
        Property("type", StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["q"] = "account"
        params["account"] = "urn:li:sponsoredAccount:" + self.config.get("account_id")
        params["owner"] = "urn:li:organization:" + self.config.get("owner")

        return params


class accountUsers(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-account-users#find-ad-account-users-by-accounts
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    columns = [
        "ACCOUNT",
        "ACCOUNT_ID",
        "CAMPAIGN_CONTACT",
        "CHANGE_AUDIT_STAMPS",
        "CREATED_TIME",
        "LAST_MODIFIED_TIME",
        "ROLE",
        "USER",
        "USER_PERSON_ID",
    ]

    name = "account_user"
    replication_keys = ["last_modified_time"]
    replication_method = "incremental"
    primary_keys = ["last_modified_time"]
    path = "adAccountUsers"

    schema = PropertiesList(
        Property("account", StringType),
        Property("campaign_contact", BooleanType),
        Property("account_id", IntegerType),
        Property(
            "changeAuditStamps",
            ObjectType(
                Property(
                    "created",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
                Property(
                    "lastModified",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
            ),
        ),
        Property("created_time", StringType),
        Property("last_modified_time", StringType),
        Property("role", StringType),
        Property("user", StringType),
        Property("user_person_id", StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["q"] = "accounts"
        params["accounts"] = "urn:li:sponsoredAccount:" + self.config.get("account_id")

        return params


class campaignGroups(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaign-groups#search-for-campaign-groups
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    name = "campaign_groups"
    replication_keys = ["last_modified_time"]
    replication_method = "incremental"
    primary_keys = ["last_modified_time", "id"]
    path = "adCampaignGroups"

    PropertiesList = th.PropertiesList
    Property = th.Property
    ObjectType = th.ObjectType
    DateTimeType = th.DateTimeType
    StringType = th.StringType
    ArrayType = th.ArrayType
    BooleanType = th.BooleanType
    IntegerType = th.IntegerType

    jsonschema = PropertiesList(
        Property(
            "runSchedule",
            ObjectType(Property("start", DateTimeType), Property("end", DateTimeType)),
        ),
        Property(
            "changeAuditStamps",
            ObjectType(
                Property(
                    "created",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
                Property(
                    "lastModified",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
            ),
        ),
        Property("created_time", DateTimeType),
        Property("last_modified_time", DateTimeType),
        Property("name", StringType),
        Property("servingStatuses", ArrayType(StringType)),
        Property("backfilled", BooleanType),
        Property("id", IntegerType),
        Property("account", StringType),
        Property("account_id", IntegerType),
        Property("status", StringType),
        Property(
            "total_budget",
            ObjectType(
                Property("currency_code", StringType), Property("amount", StringType)
            ),
        ),
        Property("test", BooleanType),
        Property("allowed_campaign_types", ArrayType(StringType)),
        Property("run_schedule_start", DateTimeType),
        Property("run_schedule_end", StringType),
    ).to_dict()

    schema = jsonschema

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["q"] = "search"
        params["sort.field"] = "ID"
        params["sort.order"] = "ASCENDING"

        return params


class campaigns(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns#search-for-campaigns
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    name = "campaign"
    replication_keys = ["last_modified_time"]
    replication_method = "incremental"
    primary_keys = ["last_modified_time", "id"]
    path = "adCampaigns"

    schema = PropertiesList(
        Property(
            "targeting",
            ObjectType(
                Property(
                    "created",
                    ObjectType(
                        Property(
                            "included_targeting_facets",
                            th.ArrayType(
                                Property(
                                    "items",
                                    ObjectType(
                                        Property("type", StringType),
                                        Property(
                                            "values",
                                            th.ArrayType(Property("items", StringType)),
                                        ),
                                        additional_properties=False,
                                    ),
                                ),
                            ),
                        ),
                        Property(
                            "excluded_targeting_facets",
                            th.ArrayType(
                                Property(
                                    "items",
                                    ObjectType(
                                        Property("type", StringType),
                                        Property(
                                            "values",
                                            th.ArrayType(Property("items", StringType)),
                                        ),
                                        additional_properties=False,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        Property(
            "targetingCriteria",
            ObjectType(
                Property(
                    "include",
                    ObjectType(
                        Property(
                            "and",
                            th.ArrayType(
                                Property(
                                    "items",
                                    ObjectType(
                                        Property("type", StringType),
                                        Property(
                                            "values",
                                            th.ArrayType(Property("items", StringType)),
                                        ),
                                        additional_properties=False,
                                    ),
                                ),
                            ),
                        ),
                        Property(
                            "or",
                            th.ArrayType(
                                Property(
                                    "items",
                                    ObjectType(
                                        Property("type", StringType),
                                        Property(
                                            "values",
                                            th.ArrayType(Property("items", StringType)),
                                        ),
                                        additional_properties=False,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Property(
                    "exclude",
                    ObjectType(
                        Property(
                            "or",
                            ObjectType(
                                Property(
                                    "urn:li:ad_targeting_facet:titles",
                                    th.ArrayType(
                                        Property("items", StringType),
                                    ),
                                ),
                                Property(
                                    "urn:li:ad_targeting_facet:staff_count_ranges",
                                    th.ArrayType(
                                        Property("items", StringType),
                                    ),
                                ),
                                Property(
                                    "urn:li:ad_targeting_facet:followed_companies",
                                    th.ArrayType(
                                        Property("items", StringType),
                                    ),
                                ),
                                Property(
                                    "urn:li:ad_targeting_facet:seniorities",
                                    th.ArrayType(
                                        Property("items", StringType),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        Property("servingStatuses", th.ArrayType(Property("items", StringType))),
        Property(
            "totalBudget",
            ObjectType(
                Property("amount", StringType),
                Property("currencyCode", StringType),
                additional_properties=False,
            ),
        ),
        Property("version_tag", StringType),
        Property(
            "locale",
            ObjectType(
                Property("country", StringType),
                Property("language", StringType),
                additional_properties=False,
            ),
        ),
        Property(
            "version",
            ObjectType(Property("versionTag", StringType), additional_properties=False),
        ),
        Property("associatedEntity", StringType),
        Property("associated_entity_organization_id", IntegerType),
        Property("associated_entity_person_id", IntegerType),
        Property(
            "runSchedule",
            ObjectType(
                Property("start", StringType),
                Property("end", StringType),
                additional_properties=False,
            ),
        ),
        Property("optimizationTargetType", StringType),
        Property(
            "changeAuditStamps",
            ObjectType(
                Property(
                    "created",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
                Property(
                    "lastModified",
                    ObjectType(
                        Property("time", StringType), additional_properties=False
                    ),
                ),
            ),
        ),
        Property("campaignGroup", StringType),
        Property("campaign_group_id", IntegerType),
        Property(
            "dailyBudget",
            ObjectType(
                Property("amount", StringType),
                Property("currencyCode", StringType),
                additional_properties=False,
            ),
        ),
        Property(
            "unitCost",
            ObjectType(
                Property("amount", StringType),
                Property("currencyCode", StringType),
                additional_properties=False,
            ),
        ),
        Property("creativeSelection", StringType),
        Property("costType", StringType),
        Property("name", StringType),
        Property("objectiveType", StringType),
        Property("offsiteDeliveryEnabled", BooleanType),
        Property(
            "offsitePreferences",
            ObjectType(
                Property(
                    "iabCategories",
                    ObjectType(
                        Property(
                            "exclude",
                            th.ArrayType(
                                Property("items", StringType),
                            ),
                        ),
                        Property(
                            "include", th.ArrayType(Property("items", StringType))
                        ),
                    ),
                ),
                Property(
                    "publisherRestrictionFiles",
                    ObjectType(
                        Property(
                            "exclude", th.ArrayType(Property("items", StringType))
                        ),
                    ),
                ),
            ),
        ),
        Property("id", IntegerType),
        Property("audienceExpansionEnabled", BooleanType),
        Property("test", BooleanType),
        Property("format", StringType),
        Property("pacingStrategy", StringType),
        Property("account", StringType),
        Property("account_id", IntegerType),
        Property("status", StringType),
        Property("type", StringType),
        Property("storyDeliveryEnabled", BooleanType),
        Property("created_time", DateTimeType),
        Property("last_modified_time", DateTimeType),
        Property("run_schedule_start", DateTimeType),
        Property("run_schedule_end", StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["q"] = "search"
        params["sort.field"] = "ID"
        params["sort.order"] = "ASCENDING"

        return params


class creatives(LinkedInStream):
    """
    https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-creatives?view=li-lms-2023-01&tabs=http#search-for-creatives
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    name = "creatives"
    replication_keys = ["last_modified_time"]
    replication_method = "incremental"
    primary_keys = ["last_modified_time", "id"]
    path = "creatives"

    schema = PropertiesList(
        Property("account", StringType),
        Property("account_id", IntegerType),
        Property("campaign", StringType),
        Property("campaign_id", IntegerType),
        Property(
            "content",
            ObjectType(
                Property("reference", StringType),
                Property(
                    "text_ad",
                    ObjectType(
                        Property("headline", StringType),
                        Property("description", StringType),
                        Property("landing_page", StringType),
                        additional_properties=False,
                    ),
                ),
            ),
        ),
        Property("created_at", StringType),
        Property("created_by", StringType),
        Property("last_modified_at", StringType),
        Property("last_modified_by", StringType),
        Property("id", StringType),
        Property("intended_status", StringType),
        Property("is_serving", BooleanType),
        Property("is_test", BooleanType),
        Property("serving_hold_reasons", th.ArrayType(Property("items", StringType))),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        ## TODO: Resolve issue with parentheses in campaigns parameter being encoded by rest.py
        params["campaigns"] = "urn:li:sponsoredCampaign:" + self.config.get("campaign")
        params["q"] = "criteria"

        return params


class adAnalyticsByCreativeInit(LinkedInStream):
    """
    https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting#analytics-finder
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_keys = datetime keys for replication
    """

    name = "AdAnalyticsByCreativeInit"
    replication_keys = ["dateRange"]
    replication_method = "incremental"
    primary_keys = ["creative_id", "dateRange"]
    path = "adAnalytics"

    schema = PropertiesList(
        Property("landingPageClicks", IntegerType),
        Property("reactions", IntegerType),
        Property("adUnitClicks", IntegerType),
        Property("creative_id", IntegerType),
        Property("documentCompletions", IntegerType),
        Property("documentFirstQuartileCompletions", IntegerType),
        Property("clicks", IntegerType),
        Property("documentMidpointCompletions", IntegerType),
        Property("documentThirdQuartileCompletions", IntegerType),
        Property("downloadClicks", IntegerType),
        Property("jobApplications", StringType),
        Property("jobApplyClicks", StringType),
        Property("postViewJobApplications", StringType),
        Property("costInUsd", StringType),
        Property("postViewRegistrations", StringType),
        Property("registrations", StringType),
        Property("talentLeads", IntegerType),
        Property("viralDocumentCompletions", IntegerType),
        Property("viralDocumentFirstQuartileCompletions", IntegerType),
        Property("viralDocumentMidpointCompletions", IntegerType),
        Property("viralDocumentThirdQuartileCompletions", IntegerType),
        Property("viralDownloadClicks", IntegerType),
        Property("viralJobApplications", StringType),
        Property("viralJobApplyClicks", StringType),
        Property("costInLocalCurrency", StringType),
        Property("viralRegistrations", IntegerType),
        Property("approximateUniqueImpressions", IntegerType),
        Property("cardClicks", IntegerType),
        Property("cardImpressions", IntegerType),
        Property("commentLikes", IntegerType),
        Property("viralCardClicks", IntegerType),
        Property("viralCardImpressions", IntegerType),
        Property("viralCommentLikes", IntegerType),

        Property("actionClicks", IntegerType),
        Property("comments", IntegerType),
        Property("companyPageClicks", IntegerType),
        Property("conversionValueInLocalCurrency", StringType),

        Property(
            "dateRange",
            ObjectType(
                Property(
                    "end",
                    ObjectType(
                        Property("day", IntegerType),
                        Property("month", IntegerType),
                        Property("year", IntegerType),
                        additional_properties=False,
                    ),
                ),
                Property(
                    "start",
                    ObjectType(
                        Property("day", IntegerType),
                        Property("month", IntegerType),
                        Property("year", IntegerType),
                        additional_properties=False,
                    ),
                ),
            ),
        ),

        Property("day", StringType),
        Property("externalWebsiteConversions", IntegerType),
        Property("externalWebsitePostClickConversions", IntegerType),
        Property("externalWebsitePostViewConversions", IntegerType),
        Property("follows", IntegerType),
        Property("fullScreenPlays", IntegerType),
        Property("impressions", IntegerType),
        Property("landingPageClicks", IntegerType),
        Property("leadGenerationMailContactInfoShares", IntegerType),
        Property("leadGenerationMailInterestedClicks", IntegerType),
        Property("likes", IntegerType),
        Property("oneClickLeadFormOpens", IntegerType),
        Property("oneClickLeads", IntegerType),
        Property("opens", IntegerType),
        Property("otherEngagements", IntegerType),
        Property("pivot", StringType),
        Property("pivotValue", StringType),
        Property("sends", IntegerType),
        Property("shares", IntegerType),
        Property("textUrlClicks", IntegerType),
        Property("totalEngagements", IntegerType),
        Property("videoCompletions", IntegerType),
        Property("videoFirstQuartileCompletions", IntegerType),
        Property("videoMidpointCompletions", IntegerType),
        Property("videoStarts", IntegerType),
        Property("videoThirdQuartileCompletions", IntegerType),
        Property("videoViews", IntegerType),
        Property("viralClicks", IntegerType),
        Property("viralComments", IntegerType),
        Property("viralCompanyPageClicks", IntegerType),
        Property("viralExternalWebsiteConversions", IntegerType),
        Property("viralExternalWebsitePostClickConversions", IntegerType),
        Property("viralExternalWebsitePostViewConversions", IntegerType),
        Property("viralFollows", IntegerType),
        Property("viralFullScreenPlays", IntegerType),
        Property("viralImpressions", IntegerType),
        Property("viralLandingPageClicks", IntegerType),
        Property("viralLikes", IntegerType),
        Property("viralOneClickLeadFormOpens", IntegerType),
        Property("viralOneclickLeads", IntegerType),
        Property("viralOtherEngagements", IntegerType),
        Property("viralReactions", IntegerType),
        Property("viralShares", IntegerType),
        Property("viralTotalEngagements", IntegerType),
        Property("viralVideoCompletions", IntegerType),
        Property("viralVideoFirstQuartileCompletions", IntegerType),
        Property("viralVideoMidpointCompletions", IntegerType),
        Property("viralVideoStarts", IntegerType),
        Property("viralVideoThirdQuartileCompletions", IntegerType),
        Property("viralVideoViews", IntegerType),

    ).to_dict()

    @property
    def adanalyticscolumns(self):
        columns = [
            "viralLandingPageClicks,viralExternalWebsitePostClickConversions,externalWebsiteConversions,viralVideoFirstQuartileCompletions,leadGenerationMailContactInfoShares,clicks,viralClicks,shares,viralFullScreenPlays,videoMidpointCompletions,viralCardClicks,viralExternalWebsitePostViewConversions,viralTotalEngagements,viralCompanyPageClicks,actionClicks,viralShares,videoCompletions,comments,externalWebsitePostViewConversions,dateRange",
            "costInUsd,landingPageClicks,oneClickLeadFormOpens,talentLeads,sends,viralOneClickLeadFormOpens,conversionValueInLocalCurrency,viralFollows,otherEngagements,viralVideoCompletions,cardImpressions,leadGenerationMailInterestedClicks,opens,totalEngagements,videoViews,viralImpressions,viralVideoViews,commentLikes,pivot,viralLikes",
            "adUnitClicks,videoThirdQuartileCompletions,cardClicks,likes,viralComments,viralVideoMidpointCompletions,viralVideoThirdQuartileCompletions,oneClickLeads,fullScreenPlays,viralCardImpressions,follows,videoStarts,videoFirstQuartileCompletions,textUrlClicks,pivotValue,reactions,viralReactions,externalWebsitePostClickConversions,viralOtherEngagements,costInLocalCurrency",
            "viralVideoStarts,viralRegistrations,viralJobApplyClicks,viralJobApplications,jobApplications,jobApplyClicks,viralExternalWebsiteConversions,postViewRegistrations,companyPageClicks,documentCompletions,documentFirstQuartileCompletions,documentMidpointCompletions,documentThirdQuartileCompletions,downloadClicks,viralDocumentCompletions,viralDocumentFirstQuartileCompletions,viralDocumentMidpointCompletions,viralDocumentThirdQuartileCompletions,viralDownloadClicks,impressions",
        ]

        return columns

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["fields"] = columns[0]


        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CREATIVE"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        # This function extracts day, month, and year from date rannge column
        # These values are aprsed with datetime function and the date is added to the day column
        try:
            daterange_day = row.get("dateRange").get("start").get("day")
            daterange_month = row.get("dateRange").get("start").get("month")
            daterange_year = row.get("dateRange").get("start").get("year")
            daterange_column = "{}-{}-{}".format(
                daterange_year, daterange_month, daterange_day
            )
            row["day"] = datetime.strptime(daterange_column, "%Y-%m-%d")
        except:
            pass
        try:
            creative_column = row.get("pivotValue")
            creative_column = int(creative_column.split(":")[3])
            row["creative_id"] = creative_column
        except:
            pass

        return super().post_process(row, context)


class adAnalyticsByCreative(adAnalyticsByCreativeInit):
    name = "ad_analytics_by_creative"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CREATIVE"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["fields"] = columns[1]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """Return a dictionary of records from adanalytics classes

        Args:
            context: The stream context.

        Returns:
            A dictionary of records given from adanalytics streams
            Adanalytics classes: adanalyticsinit_stream, adanalyticsecond_stream, adanalyticsthird_stream
            Adanalytics classes gives a dictionary of records with 20 columns
            super() calls the records of adAnalyticsByCampaign class
            These classes are generator objects so they can't be merged unless we convert them into lists
            list() converts generator objects into lists
            merge_dicts() merges these classes
        """
        adanalyticsinit_stream = adAnalyticsByCreativeInit(
            self._tap, schema={"properties": {}}
        )
        adanalyticsecond_stream = adAnalyticsByCreativeSecond(
            self._tap, schema={"properties": {}}
        )
        adanalyticsthird_stream = adAnalyticsByCreativeThird(
            self._tap, schema={"properties": {}}
        )
        adanalytics_records = [
            self.merge_dicts(x, y, z, p)
            for x, y, z, p in zip(
                list(adanalyticsinit_stream.get_records(context)),
                list(super().get_records(context)),
                list(adanalyticsecond_stream.get_records(context)),
                list(adanalyticsthird_stream.get_records(context)),
            )
        ]

        return adanalytics_records

    def merge_dicts(self, *dict_args):
        """
        Given any number of dictionaries, shallow copy and merge into a new dict,
        precedence goes to key-value pairs in latter dictionaries.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result


class adAnalyticsByCreativeSecond(adAnalyticsByCreativeInit):
    name = "adanalyticsbycreative_second"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CREATIVE"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["fields"] = columns[2]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )

        return params


class adAnalyticsByCreativeThird(adAnalyticsByCreativeInit):
    name = "adanalyticsbycreative_third"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        columns = self.adanalyticscolumns

        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        start_date = pendulum.parse(self.config.get("start_date"))
        end_date = pendulum.parse(self.config.get("end_date"))

        params["q"] = "analytics"
        params["pivot"] = "CREATIVE"
        params["timeGranularity"] = "DAILY"
        params["dateRange.start.day"] = start_date.day
        params["dateRange.start.month"] = start_date.month
        params["dateRange.start.year"] = start_date.year
        params["dateRange.end.day"] = end_date.day
        params["dateRange.end.month"] = end_date.month
        params["dateRange.end.year"] = end_date.year
        params["fields"] = columns[3]
        params["campaigns[0]"] = "urn:li:sponsoredCampaign:" + self.config.get(
            "campaign"
        )


        return params
