from dbt.adapters.postgres.relation_configs.index import (  # noqa: F401
    PostgresIndexConfig,
    PostgresIndexConfigChange,
)
from dbt.adapters.postgres.relation_configs.policies import (  # noqa: F401
    PostgresIncludePolicy,
    PostgresQuotePolicy,
    MAX_CHARACTERS_IN_IDENTIFIER,
)
from dbt.adapters.postgres.relation_configs.materialized_view import (  # noqa: F401
    PostgresMaterializedViewConfig,
    PostgresMaterializedViewConfigChangeset,
)
