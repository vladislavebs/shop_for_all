# Date created filter
import coreschema

from shop_for_all.helpers.filters_backends import Filter, FiltersGroup

# Data filter
date_gte_filter = Filter(
    name="date_gte",
    query_filter="date_created__gte",
    schema=coreschema.String(title="Start date", description="Start date."),
)

date_lte_filter = Filter(
    name="date_lte",
    query_filter="date_created__lte",
    schema=coreschema.String(title="End date", description="End date."),
)

date_filter = FiltersGroup(date_gte_filter, date_lte_filter)


# Amount filter
amount_gte_filter = Filter(
    name="amount_gte",
    query_filter="amount__gte",
    schema=coreschema.String(title="Min amount", description="Min amount."),
)

amount_lte_filter = Filter(
    name="amount_lte",
    query_filter="amount__lte",
    schema=coreschema.Number(title="Max amount", description="Max amount."),
)

amount_filter = FiltersGroup(date_gte_filter, date_lte_filter)
