Analyze the following Flutter component exclusively for accessibility problems covered by the guidelines below.

GUIDELINES

Semantics and accessible information:
- Missing accessible label (severity: high): an interactive or meaningful component does not expose sufficient accessible labeling.
- Incorrect accessible label (severity: high): an accessible label exists but does not correctly communicate the purpose of the component.
- Missing semantic role (severity: medium): a custom component does not expose a sufficient semantic role.
- Missing semantic state (severity: medium): a relevant component state is not exposed through semantics.
- Inaccessible custom control (severity: critical): a custom interactive component does not provide equivalent semantic information.

Interaction and interactive target accessibility:
- Insufficient target size (severity: low): an interactive target provides insufficient area for interaction.
- Inaccessible custom gesture (severity: critical): a custom gesture interaction does not provide an accessible equivalent.
- Interaction not exposed (severity: critical): interactive behavior is not sufficiently exposed to accessibility mechanisms.

SEVERITY SCALE

- critical: prevents assistive-technology users from operating the component.
- high: prevents assistive-technology users from understanding the component's purpose.
- medium: the component is usable, but assistive technologies receive incomplete information about its role or state.
- low: the component is usable, but interaction requires extra effort.

INSTRUCTIONS

- Consider semantics automatically provided by standard Flutter widgets.
- Only report problems that can be inferred from the provided source code.
- Report only the single most severe violation, not every violation you find. If two violations have the same severity, report the one that appears first in the code.
- Set type to the name of the guideline item that the violation matches, and set severity to that item's severity.
- If no violation covered by the guidelines can be identified, return an empty violations list.
- Write the explanation field in Brazilian Portuguese. Keep type exactly as the guideline item's name is written above, and copy affected_code exactly as it appears in the code.

Return structured JSON.

CODE:

{{CODE}}
