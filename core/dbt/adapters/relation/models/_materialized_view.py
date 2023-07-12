from dataclasses import dataclass, field

from dbt.contracts.relation import RelationType
from dbt.exceptions import DbtRuntimeError

from dbt.adapters.relation.models._change import RelationChangeset
from dbt.adapters.relation.models._policy import RenderPolicy
from dbt.adapters.relation.models._relation import Relation
from dbt.adapters.relation.models._schema import SchemaRelation


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class MaterializedViewRelation(Relation):
    """
    This config serves as a default implementation for materialized views. It's bare bones and only
    supports the minimal attribution and drop/create (no alter). This may suffice for your needs.
    However, if your adapter requires more attribution, it's recommended to subclass directly
    from `Relation` and bypass this default; don't subclass from this.

    *Note:* Even if you use this, you'll still need to provide query templates for the macros
    found in `include/global_project/macros/relations/atomic/*.sql` as there is no way to predict
    that target database platform's data structure.

    The following parameters are configurable by dbt:
    - name: name of the materialized view
    - schema: schema that contains the materialized view
    - query: the query that defines the view
    """

    # attribution
    name: str
    schema: SchemaRelation
    query: str = field(hash=False, compare=False)

    # configuration
    type = RelationType.MaterializedView
    render = RenderPolicy()
    SchemaParser = SchemaRelation
    can_be_renamed = False

    @classmethod
    def from_dict(cls, config_dict: dict) -> "MaterializedViewRelation":
        """
        Creates an instance of this class given the dict representation

        This is generally used indirectly by calling either `from_model_node()` or `from_relation_results()`

        Args:
            config_dict: a dict that aligns with the structure of this class

        Returns: an instance of this class
        """
        materialized_view = super().from_dict(config_dict)
        assert isinstance(materialized_view, MaterializedViewRelation)
        return materialized_view


@dataclass
class MaterializedViewRelationChangeset(RelationChangeset):
    @classmethod
    def parse_relations(cls, existing_relation: Relation, target_relation: Relation) -> dict:
        try:
            assert isinstance(existing_relation, MaterializedViewRelation)
            assert isinstance(target_relation, MaterializedViewRelation)
        except AssertionError:
            raise DbtRuntimeError(
                f"Two materialized view relations were expected, but received:\n"
                f"    existing: {existing_relation}\n"
                f"    new: {target_relation}\n"
            )
        return {}

    @property
    def requires_full_refresh(self) -> bool:
        return True

    @property
    def is_empty(self) -> bool:
        return False
