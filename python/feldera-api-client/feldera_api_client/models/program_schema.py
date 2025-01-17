from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define, field

if TYPE_CHECKING:
    from ..models.relation import Relation


T = TypeVar("T", bound="ProgramSchema")


@define
class ProgramSchema:
    """A struct containting the tables (inputs) and views for a program.

    Parse from the JSON data-type of the DDL generated by the SQL compiler.

        Attributes:
            inputs (List['Relation']):
            outputs (List['Relation']):
    """

    inputs: List["Relation"]
    outputs: List["Relation"]
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inputs = []
        for inputs_item_data in self.inputs:
            inputs_item = inputs_item_data.to_dict()

            inputs.append(inputs_item)

        outputs = []
        for outputs_item_data in self.outputs:
            outputs_item = outputs_item_data.to_dict()

            outputs.append(outputs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputs": inputs,
                "outputs": outputs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.relation import Relation

        d = src_dict.copy()
        inputs = []
        _inputs = d.pop("inputs")
        for inputs_item_data in _inputs:
            inputs_item = Relation.from_dict(inputs_item_data)

            inputs.append(inputs_item)

        outputs = []
        _outputs = d.pop("outputs")
        for outputs_item_data in _outputs:
            outputs_item = Relation.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        program_schema = cls(
            inputs=inputs,
            outputs=outputs,
        )

        program_schema.additional_properties = d
        return program_schema

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
