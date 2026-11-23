# Linha de base com ferramentas tradicionais (O4)

| Ferramenta | VP | FP | VN | FN | Inválidas | Revocação | Precisão | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flutter_analyze | 0 | 0 | 41 | 42 | 0 | 0.00 | 0.00 | 0.00 |
| widget_test_guidelines | 15 | 3 | 38 | 27 | 0 | 0.36 | 0.83 | 0.50 |

## Violações detectadas pelos widget tests, por subcategoria principal

| Subcategoria | Detectadas | Variantes com violação |
| --- | --- | --- |
| inaccessible_custom_control | 4 | 5 |
| inaccessible_custom_gesture | 0 | 5 |
| incorrect_accessible_label | 0 | 5 |
| insufficient_target_size | 4 | 5 |
| interaction_not_exposed | 0 | 5 |
| missing_accessible_label | 6 | 7 |
| missing_role | 1 | 5 |
| missing_state | 0 | 5 |

`flutter analyze` (flutter_lints) não tem regras de acessibilidade; regras disparadas: constant_identifier_names, use_key_in_widget_constructors. Ele é contado como sem detecção em todas as variantes.
Variantes cujo widget test não completou: 0.
